#!/usr/bin/pyhton
# -*- coding: utf-8 -*-
# @Author: xiaoli
# @Time: 2019/5/25
from base.handler import BaseHandler, GetUserHandler, CheckTokenHandler
from constant import Constants
from .models import TDictionary, SysPermission, SysUser, SysUserRole, SysRole, SysLog, WhiteBlackList, TLookupGroup, \
    SysRolePermission
from playhouse.shortcuts import model_to_dict
import io
import jwt
import hashlib
import json
import random
from PIL import Image, ImageDraw, ImageFont
import datetime
from constant import SECRET
from utils.restful import result, forbidden, params_error, ok, server_error, data
import logging
import uuid
from utils.inserlog import log


# 获取验证登陆页面的token值
class GetConfigGetLoginToken(BaseHandler):
    def prepare(self):
        self.num = random.randint(100000000, 999999999)
        payload = {'function': 'login', 'num': self.num, 'time': datetime.datetime.now().strftime("%b %d %Y %H:%M:%S")}
        self.token = str(jwt.encode(payload, SECRET, algorithm='HS256'), encoding="utf-8")
    async def post(self):
        content = result(message="获取验证登陆页面的token值正确")
        self.set_cookie('loginToken', self.token)  # 这个是jwt加密后的token值，所以明文存储没有问题
        return await self.finish(content)


# 验证码
class GetConfigCacheHandler(BaseHandler):
    async def get(self):
        """
        这个验证码的功能是，后台生成随机数，保存在django的session中，同时将这个随机数做成图片，并增加一些噪点，
        传递给前端并展示出来。
        """
        # 定义变量，用于画面的背景色、宽、高
        bgcolor = '#3D1769'
        width = 100
        height = 40
        # 创建画面对象
        im = Image.new('RGB', (width, height), bgcolor)
        # 创建画笔对象
        draw = ImageDraw.Draw(im)
        # 调用画笔的point()函数绘制噪点
        for i in range(0, 100):
            xy = (random.randrange(0, width), random.randrange(0, height))
            fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
            draw.point(xy, fill=fill)
        # 定义验证码的备选值
        str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
        # 随机选取4个值作为验证码
        rand_str = ''
        for i in range(0, 4):
            rand_str += str1[random.randrange(0, len(str1))]
        # 构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
        font = ImageFont.truetype('FreeMono.ttf', 33)  # linux
        # font = ImageFont.truetype('arial.ttf', 33)  # win7的
        # 构造字体颜色
        # 选取验证码的背景颜色
        fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
        # 绘制4个字
        draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
        draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
        draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
        draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
        # 释放画笔
        del draw
        # 存入redis，用于做进一步验证
        self.redis_conn.set(Constants["REDIS_CONFIG_CACHE_CODE"], rand_str)
        # 内存文件操作
        buf = io.BytesIO()
        # 将图片保存在内存中，文件类型为png
        im.save(buf, 'png')
        self.set_header('Content-type', 'image/png')
        # 将内存中的图片数据返回给客户端，MIME类型为图片png
        return await self.finish(buf.getvalue())


# 登陆校验并返回token值
class GetLoginHandler(BaseHandler):
    async def prepare(self):
        cookieToken = self.get_cookie('loginToken')
        headerToken = self.request.headers["X-CSRF-TOKEN"]
        if cookieToken != headerToken:
            logging.info("CSRF校验不能通过，请重试！")
            content = forbidden(message="CSRF校验不能通过，请重试！")
            return await self.finish(content)

    async def post(self):
        ip = self.request.remote_ip
        username = self.get_argument('username', '')
        # 验证用户是否在白名单中
        if not await self.application.objects.execute(WhiteBlackList.select().where(WhiteBlackList.role_type==0, WhiteBlackList.ip==ip, WhiteBlackList.user_name==username)):
            content = params_error(message="用户没有权限")
            return await self.finish(content)
        password = self.get_argument('password', None)
        text = self.get_argument('text', None)
        redis_text = self.redis_conn.get(Constants["REDIS_CONFIG_CACHE_CODE"])
        if not redis_text.lower() == text.lower():
            content = params_error(message="验证码不正确，请重试")
            return await self.finish(content)
        hl = hashlib.md5()
        if not password:
            content = params_error(message="密码不正确，请重试！")
            return await self.finish(content)
        hl.update(password.encode(encoding='utf-8'))
        password = hl.hexdigest()
        try:
            value = await self.application.objects.get(SysUser, user_name=username, password=password)
            role = await self.application.objects.execute(SysRole.select().join(SysUserRole, on=(SysRole.id == SysUserRole.role_id)).where(SysUserRole.user_id == value.id))
            if not role:
                content = params_error(message="用户没有角色，请重试！")
                return await self.finish(content)
            payload = {'function': 'usertoken', 'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'role': [i.id for i in role], 'username': username}
            token = str(jwt.encode(payload, SECRET, algorithm='HS256'), encoding="utf-8")
            self.set_cookie('token', token)
            # 设置用户的cookie信息
            session_id = uuid.uuid4().hex
            self.set_secure_cookie("session_id", session_id)
            self.redis_conn.set('sess_%s' % session_id, username)
            # 登陆日志记录
            await log(self, '登陆')
            await self.application.objects.execute(SysUser.update(last_login_time=datetime.datetime.now(), login_ip=ip).where(SysUser.id == value.id))
            content = ok()
            return await self.finish(content)
        except Exception as e:
            logging.error(e)
            content = params_error(message="用户不存在，请重试！")
            return await self.finish(content)


# 获取登陆管理员
class GetUserNameHandler(CheckTokenHandler):
    async def post(self):
        username = self.current_user
        content = result(message=username)
        return await self.finish(content)


# 获取到首页菜单
class MenuUuserMenuListHandler(GetUserHandler):
    async def get(self):
        cookie_token = self.get_cookie('token')
        role = jwt.decode(cookie_token, SECRET, algorithms='HS256')['role']
        try:
            values = await self.application.objects.execute(SysPermission.select().join(SysRolePermission, on=(SysPermission.id == SysRolePermission.pers_id)).where(SysPermission.model_level == 1, SysRolePermission.role_id.in_(role)).order_by(SysPermission.model_order))
            content = []
            for value in values:
                children = []
                childs = await self.application.objects.execute(SysPermission.select().join(SysRolePermission, on=(SysPermission.id == SysRolePermission.pers_id)).where(SysPermission.parent_id == value.id, SysRolePermission.role_id.in_(role)))
                for child in childs:
                    child_dict = {
                        "level": child.model_level,
                        "icon": child.icon,
                        "description": child.description,
                        "url": child.url,
                        "order": child.model_order
                    }
                    children.append(child_dict)
                data = {
                    "level": value.model_level,
                    "icon": value.icon,
                    "description": value.description,
                    "url": value.url,
                    "order": value.model_order,
                    "children": children
                }
                content.append(data)
            content = json.dumps(content)
            return await self.finish(content)
        except Exception as e:
            content = server_error(message="用户数据不存在，请重试")
            return await self.finish(content)


# 用户登出页面
class LogoutHandler(GetUserHandler):
    async def post(self):
        await log(self, '退出')
        self.set_cookie('token', '')
        return await self.finish(ok())


# 数据字典所有信息展示，同时承担了查询的任务
class GetConfigDictionaryListHandler(GetUserHandler):
    async def get(self):
        page = self.get_argument('page', '1')
        limit = self.get_argument('limit', '10')
        search_value = self.get_argument("searchValue", '')
        search_key = self.get_argument("searchKey", '')
        try:
            page_int = int(page)
            limit_int = int(limit)
            values = await self.application.objects.execute(TDictionary.select().where(TDictionary.dic_key.contains(search_key), TDictionary.dic_value.contains(search_value)).paginate(page_int, limit_int))
            count = await self.application.objects.count(TDictionary.select().where(TDictionary.dic_key.contains(search_key), TDictionary.dic_value.contains(search_value)))
            content = data(data=[model_to_dict(value) for value in values], kwargs={"count": count})
            return await self.finish(content)
        except Exception as e:
            content = server_error(message="字典数据不存在，请重试")
            return await self.finish(content)


# 添加数据字典
class CreateConfigDictionarySaveHandler(CheckTokenHandler):
    async def post(self):
        dic_key = self.get_argument('dicKey', None)
        dic_value = self.get_argument('dicValue', None)
        description = self.get_argument('description', None)
        ip = self.request.remote_ip
        user = self.current_user
        if not dic_value:
            content = params_error(message='这个字段必须填写')
            return await self.finish(content)
        try:
            if await self.application.objects.create(TDictionary, dic_key=dic_key, dic_value=dic_value, description=description):
                await log(self, '添加字典')
                content = result(message="添加成功")
                return await self.finish(content)
            else:
                content = params_error(message="添加失败，请重试！")
                return await self.finish(content)
        except Exception as e:
            content = params_error(message='参数传递有误，请重试！')
            return await self.finish(content)


# 删除字典数据
class DeleteConfigDictionaryDelHandler(CheckTokenHandler):
    async def post(self, id):
        try:
            if await self.application.objects.execute(TDictionary.delete().where(TDictionary.id == id)):
                await log(self, '删除字典')
                content = result(message='删除成功')
                return await self.finish(content)
            else:
                content = params_error(message='这个字典不存在')
                return await self.finish(content)
        except Exception as e:
            content = params_error(message='查找字典的时候出错了')
            return await self.finish(content)


# 修改字典数据
class UpdateConfigDictionaryUpdateHandler(CheckTokenHandler):
    async def post(self):
        id = self.get_argument('id', None)
        dic_key = self.get_argument('dicKey', None)
        dic_value = self.get_argument('dicValue', None)
        description = self.get_argument('description', None)
        try:
            if await self.application.objects.execute(TDictionary.update(dic_key=dic_key, dic_value=dic_value, description=description).where(TDictionary.id == id)):
                await log(self, '修改字典')
                content = result(message='更改成功')
                return await self.finish(content)
            else:
                content = params_error(message="修改失败，请重试！")
                return await self.finish(content)
        except Exception as e:
            content = params_error(message='参数传递有误，请重试！')
            return await self.finish(content)


# LOOKUP管理所有信息展示
class GetConfigLookUpGroupListHandler(GetUserHandler):
    async def get(self):
        page = self.get_argument('page', '1')
        limit = self.get_argument('limit', '10')
        try:
            page_int = int(page)
            limit_int = int(limit)
            values = await self.application.objects.execute(TLookupGroup.select().paginate(page_int, limit_int))
            count = await self.application.objects.count(TLookupGroup.select())
            content = data(data=[model_to_dict(value) for value in values], kwargs={"count": count})
            return await self.finish(content)
        except Exception as e:
            content = server_error(message="LOOKUP管理数据不存在，请重试")
            return await self.finish(content)


# 添加lookup数据，同修改在一个视图同
class CreateConfigLookupGroupSaveHandler(CheckTokenHandler):
    async def post(self):
        group_code = self.get_argument("groupCode", None)
        group_name = self.get_argument("groupName", None)
        state = self.get_argument("state", None)
        parent_group_code = self.get_argument("parentGroupCode", None)
        id = self.get_argument("id", None)
        if not group_code:
            content = params_error(message='这个字段必须填写')
            return await self.finish(content)
        try:
            if id:  # 修改lookup数据
                if await self.application.objects.execute(TLookupGroup.update(group_code=group_code, group_name=group_name, state=state, parent_group_code=parent_group_code).where(TLookupGroup.id == id)):
                    await log(self, '修改lookup数据')
                    content = result(message="修改成功")
                    return await self.finish(content)
                else:
                    content = params_error(message="修改失败，请重试！")
                    return await self.finish(content)
            else:  # 这个是添加lookup信息
                if await self.application.objects.create(TLookupGroup, group_code=group_code, group_name=group_name, state=state, parent_group_code=parent_group_code):
                    await log(self, '添加lookup数据')
                    content = result(message="添加成功")
                    return await self.finish(content)
                else:
                    content = params_error(message="添加失败，请重试！")
                    return await self.finish(content)
        except Exception as e:
            content = params_error(message='参数传递有误，请重试！')
            return await self.finish(content)


# 删除lookup数据
class DeleteConfigLookupGroupDeleteByIdHandler(CheckTokenHandler):
    async def post(self):
        id = self.get_argument('id', None)
        try:
            if await self.application.objects.execute(TLookupGroup.delete().where(TLookupGroup.id == id)):
                await log(self, '删除lookup数据')
                content = result(message='删除成功')
                return await self.finish(content)
            else:
                content = params_error(message='这个lookup不存在')
                return await self.finish(content)
        except Exception as e:
            content = params_error(message='查找lookup的时候出错了')
            return await self.finish(content)


# 修改lookup数据时，先查询这个lookup的信息
class GetConfigLookUpGroupInfoHandler(GetUserHandler):
    async def get(self):
        id = self.get_argument('id', '')
        try:
            value = await self.application.objects.get(TLookupGroup, id=id)
            dict_data = {
                "createTime": value.create_time,
                "createUser": value.create_user,
                "groupCode": value.group_code,
                "groupName": value.group_name,
                "id": value.id,
                "parentGroupCode": value.parent_group_code,
                "state": value.state,
                "udpateTime": value.udpate_time,
                "updateUser": value.update_user
            }
            content = data(data=dict_data)
            return await self.finish(content)
        except Exception as e:
            content = params_error(message='查找lookup的时候出错了')
            return await self.finish(content)


# 系统白名单所有信息展示，同时负责查询工作
class GetConfigBlackWhiteWhiteListHandler(GetUserHandler):
    async def get(self):
        page = self.get_argument('page', '1')
        limit = self.get_argument('limit', '10')
        key = self.get_argument('key', '')
        try:
            page_int = int(page)
            limit_int = int(limit)
            values = await self.application.objects.execute(WhiteBlackList.select().where(WhiteBlackList.role_type == 0, WhiteBlackList.user_name.contains(key)).paginate(page_int, limit_int))
            count = await self.application.objects.count(WhiteBlackList.select().where(WhiteBlackList.role_type == 0, WhiteBlackList.user_name.contains(key)))
            data_list = []
            for value in values:
                value_dict = model_to_dict(value)
                if value.create_time:
                    value_dict["createTimeStr"] = value.create_time.strftime("%Y-%m-%d %H:%M:%S")
                data_list.append(value_dict)
            content = data(data=data_list, kwargs={"count": count})
            return await self.finish(content)
        except Exception as e:
            content = server_error(message="系统白名单不存在，请重试")
            return await self.finish(content)


# 添加系统白名单数据
class CreateConfigBlackWhiteAddWhiteHandler(CheckTokenHandler):
    async def post(self):
        user_name = self.get_argument("userName", None)
        ip = self.get_argument("ip", None)
        remarks = self.get_argument("remarks", None)
        try:
            if await self.application.objects.create(WhiteBlackList, ip=ip, user_name=user_name, remarks=remarks, role_type=0):
                await log(self, '添加系统白名单')
                content = result(message="添加成功")
                return await self.finish(content)
            else:
                content = params_error(message="添加失败，请重试！")
                return await self.finish(content)
        except Exception as e:
            content = params_error(message='参数传递有误，请重试！')
            return await self.finish(content)


# 删除系统白名单数据
class DeleteConfigBlackWhiteDeleteHandler(CheckTokenHandler):
    async def post(self):
        id = self.get_argument('id', None)
        try:
            if await self.application.objects.execute(WhiteBlackList.delete().where(WhiteBlackList.id == id)):
                await log(self, '删除系统白名单')
                content = result(message='删除成功')
                return await self.finish(content)
            else:
                content = params_error(message='这个系统名单不存在')
                return await self.finish(content)
        except Exception as e:
            content = params_error(message='查找系统名单的时候出错了')
            return await self.finish(content)


# 删除多个系统黑白名单
class DeleteConfigBlackWhiteBatchDeleteHandler(CheckTokenHandler):
    async def post(self):
        ids = self.get_argument('ids', None)
        try:
            id_list = ids.split(',')
            if await self.application.objects.execute(WhiteBlackList.delete().where(WhiteBlackList.id.in_(id_list))):
                await log(self, '删除系统多个黑白名单')
                content = result(message='删除成功')
                return await self.finish(content)
            else:
                content = params_error(message='这个系统白名单不存在')
                return await self.finish(content)
        except Exception as e:
            content = params_error(message='查找系统白名单的时候出错了')
            return await self.finish(content)


# 用户黑名单所有信息展示，同时负责查询工作
class GetConfigBlackWhiteBlackListHandler(GetUserHandler):
    async def get(self):
        page = self.get_argument('page', '1')
        limit = self.get_argument('limit', '10')
        key = self.get_argument('key', '')
        try:
            page_int = int(page)
            limit_int = int(limit)
            values = await self.application.objects.execute(WhiteBlackList.select().where(WhiteBlackList.role_type == 1, WhiteBlackList.user_name.contains(key)).paginate(page_int, limit_int))
            count = await self.application.objects.count(WhiteBlackList.select().where(WhiteBlackList.role_type == 1, WhiteBlackList.user_name.contains(key)))
            data_list = []
            for value in values:
                value_dict = model_to_dict(value)
                if value.create_time:
                    value_dict["createTimeStr"] = value.create_time.strftime("%Y-%m-%d %H:%M:%S")
                data_list.append(value_dict)
            content = data(data=data_list, kwargs={"count": count})
            return await self.finish(content)
        except Exception as e:
            content = params_error(message='参数传递有误，请重试！')
            return await self.finish(content)


# 添加用户黑名单
class CreateConfigBlackWhiteAddBlackHandler(CheckTokenHandler):
    async def post(self):
        user_name = self.get_argument("userName", None)
        ip = self.get_argument("ip", None)
        remarks = self.get_argument("remarks", None)
        try:
            if await self.application.objects.create(WhiteBlackList, ip=ip, user_name=user_name, remarks=remarks, role_type=1):
                await log(self, '添加系统黑名单')
                content = result(message="添加成功")
                return await self.finish(content)
            else:
                content = params_error(message="添加失败，请重试！")
                return await self.finish(content)
        except Exception as e:
            content = params_error(message='参数传递有误，请重试！')
            return await self.finish(content)


# 日志管理所有信息展示
class GetSysLogListHandler(GetUserHandler):
    async def get(self):
        page = self.get_argument('page', '1')
        limit = self.get_argument('limit', '10')
        log_user = self.get_argument('logUser', None)
        create_time = self.get_argument('createTime', None)
        end_time = self.get_argument('endTime', None)
        try:
            page_int = int(page)
            limit_int = int(limit)
            if end_time is not None or create_time is not None or log_user is not None:
                end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S") if end_time else ''
                create_time = datetime.datetime.strptime(create_time, "%Y-%m-%d %H:%M:%S") if create_time else ''
                if create_time:
                    values = await self.application.objects.execute(SysLog.select().where(SysLog.create_time <= end_time, SysLog.create_time >= create_time, SysLog.log_user.contains(log_user)).paginate(page_int, limit_int))
                    count = await self.application.objects.count(SysLog.select().where(SysLog.create_time <= end_time, SysLog.create_time >= create_time, SysLog.log_user.contains(log_user)))
                else:
                    values = await self.application.objects.execute(SysLog.select().where(SysLog.create_time <= end_time, SysLog.log_user.contains(log_user)).paginate(page_int, limit_int))
                    count = await self.application.objects.count(SysLog.select().where(SysLog.create_time <= end_time, SysLog.log_user.contains(log_user)))
            else:
                values = await self.application.objects.execute(SysLog.select().paginate(page_int, limit_int))
                count = await self.application.objects.count(SysLog.select())
            data_list = []
            for value in values:
                value_dict = model_to_dict(value)
                value_dict["createTimeStr"] = value.create_time.strftime("%Y-%m-%d %H:%M:%S")
                data_list.append(value_dict)
            content = data(data=data_list, kwargs={"count": count})
            return await self.finish(content)
        except Exception as e:
            content = params_error(message='参数传递有误，请重试！')
            return await self.finish(content)


# 删除多个日志管理记录
class DeleteConfigSysLogBatchDeleteHandler(CheckTokenHandler):
    async def post(self):
        ids = self.get_argument('logIds', None)
        try:
            id_list = ids.split(',')
            if await self.application.objects.execute(SysLog.delete().where(SysLog.id.in_(id_list))):
                await log(self, '删除多个日志管理记录')
                content = result(message='删除成功')
                return await self.finish(content)
            else:
                content = params_error(message='这个日志记录不存在')
                return await self.finish(content)
        except Exception as e:
            content = params_error(message='查找日志记录的时候出错了')
            return await self.finish(content)


# 清空日志管理记录
class DeleteConfigSysLogClearLogHandler(CheckTokenHandler):
    async def post(self):
        try:
            if await self.application.objects.execute(SysLog.delete()):
                await log(self, '清空日志管理记录')
                content = result(message='删除成功')
                return await self.finish(content)
            else:
                content = params_error(message='这个日志记录不存在')
                return await self.finish(content)
        except Exception as e:
            content = params_error(message='查找日志记录的时候出错了')
            return await self.finish(content)


# 菜单管理所有信息展示
class PermissionListHandler(GetUserHandler):
    async def get(self):
        page = self.get_argument('page', None)
        limit = self.get_argument('limit', None)
        key = self.get_argument('key', '')
        try:
            if page is not None or limit is not None:
                if page == '' or limit == '':
                    page = 1
                    limit = 10
                else:
                    page = int(page)
                    limit = int(limit)
                value = await self.application.objects.execute(SysPermission.select().where(SysPermission.description.contains(key)).paginate(page, limit))
                count = await self.application.objects.count(SysPermission.select().where(SysPermission.description.contains(key)))
            else:
                value = await self.application.objects.execute(SysPermission.select().where(SysPermission.description.contains(key)))
                count = len(value)
            content = data(data=[model_to_dict(i) for i in value], kwargs={"count": count})
            await self.finish(content)
        except SysPermission.DoesNotExist:
            content = server_error(message="菜单管理所有信息不存在，请重试")
            return await self.finish(content)


# 添加菜单管理
class CreateConfigSysPermissionHandler(CheckTokenHandler):
    async def post(self):
        description = self.get_argument('description', None)
        url = self.get_argument('url', None)
        icon = self.get_argument('icon', None)
        parent_id = self.get_argument('parentId', None)
        model_order = self.get_argument('modelOrder', None)
        try:
            if await self.application.objects.create(SysPermission, description=description, url=url, icon=icon, parent_id=parent_id, model_order=model_order):
                await log(self, '添加菜单管理')
                content = result(message="添加成功")
                return await self.finish(content)
            else:
                content = params_error(message="添加失败，请重试！")
                return await self.finish(content)
        except Exception as e:
            content = params_error(message='参数传递有误，请重试！')
            return await self.finish(content)


# 删除菜单管理
class DeleteConfigSysPermissionHandler(CheckTokenHandler):
    async def post(self):
        id = self.get_argument('id', None)
        try:
            if await self.application.objects.execute(SysPermission.delete().where(SysPermission.id == id)):
                await log(self, '删除菜单管理')
                content = result(message='删除成功')
                return await self.finish(content)
            else:
                content = params_error(message='这个菜单管理名单不存在')
                return await self.finish(content)
        except Exception as e:
            content = params_error(message='查找菜单管理的时候出错了')
            return await self.finish(content)


# 修改菜单管理
class UpdateConfigSysPermissionHandler(CheckTokenHandler):
    async def post(self):
        id = self.get_argument('id', None)
        description = self.get_argument('description', None)
        url = self.get_argument('url', None)
        icon = self.get_argument('icon', None)
        parent_id = self.get_argument('parentId', None)
        model_order = self.get_argument('modelOrder', None)
        try:
            if await self.application.objects.execute(SysPermission.update(description=description, url=url, icon=icon, parent_id=parent_id, model_order=model_order).where(SysPermission.id == id)):
                await log(self, '修改菜单管理')
                content = result(message='更改成功')
                return await self.finish(content)
            else:
                content = params_error(message="修改失败，请重试！")
                return await self.finish(content)
        except Exception as e:
            content = params_error(message='参数传递有误，请重试！')
            return await self.finish(content)


# 角色管理所有信息展示
class GetSysRoleListHandler(GetUserHandler):
    async def get(self):
        page = self.get_argument('page', '1')
        limit = self.get_argument('limit', '10')
        key = self.get_argument('key', '')
        try:
            page_int = int(page)
            limit_int = int(limit)
            values = await self.application.objects.execute(SysRole.select().where(SysRole.role_name.contains(key)).paginate(page_int, limit_int))
            count = await self.application.objects.count(SysRole.select().where(SysRole.role_name.contains(key)))
            content = data(data=[model_to_dict(i) for i in values], kwargs={"count": count})
            await self.finish(content)
        except Exception as e:
            content = server_error(message="角色管理所有信息不存在，请重试")
            return await self.finish(content)


# 添加角色管理
class CreateConfigSysRoleHandler(CheckTokenHandler):
    async def post(self):
        role_name = self.get_argument('roleName', None)
        role_desc = self.get_argument('roleDesc', None)
        ids = self.get_arguments('id')
        try:
            value = await self.application.objects.create(SysRole, role_name=role_name, role_desc=role_desc)
            for id in ids:
                await self.application.objects.create(SysRolePermission, role_id=value.id, pers_id=id)
            await log(self, '添加角色管理')
            content = result(message="添加成功")
            return await self.finish(content)
        except Exception as e:
            content = params_error(message='参数传递有误，请重试！')
            return await self.finish(content)


# 删除角色管理
class DeleteConfigSysRoleHandler(CheckTokenHandler):
    async def post(self):
        id = self.get_argument('id', None)
        try:
            await self.application.objects.execute(SysRolePermission.delete().where(SysRolePermission.role_id == id))
            await self.application.objects.execute(SysRole.delete().where(SysRole.id == id))
            await log(self, '删除角色管理')
            content = result(message='删除成功')
            return await self.finish(content)
        except Exception as e:
            content = params_error(message='查找菜单管理的时候出错了')
            return await self.finish(content)


# 修改角色管理之前，需要查看角色由什么权限
class GetConfigSysRoleQueryPermissionHandler(CheckTokenHandler):
    async def get(self):
        id = self.get_argument('roleId', None)
        try:
            values = await self.application.objects.execute(SysRolePermission.select().where(SysRolePermission.role_id==id))
            str = ','.join(["%s" % value.pers_id for value in values])
            content = result(data=str)
            await self.finish(content)
        except Exception as e:
            content = server_error(message="角色权限不存在，请重试")
            return await self.finish(content)


# 修改角色管理
class UpdateConfigSysRoleHandler(CheckTokenHandler):
    async def post(self):
        ids = self.get_arguments('id')
        role_id = self.get_argument('roleId')
        role_name = self.get_argument('roleName')
        role_desc = self.get_argument('roleDesc')
        try:
            await self.application.objects.execute(SysRole.update(role_name=role_name, role_desc=role_desc).where(SysRole.id == role_id))
            await self.application.objects.execute(SysRolePermission.delete().where(SysRolePermission.role_id == role_id))
            for id in ids:
                await self.application.objects.create(SysRolePermission, role_id=role_id, pers_id=id)
            await log(self, '修改角色管理')
            content = result(message="更改成功")
            return await self.finish(content)
        except Exception as e:
            content = params_error(message='更改的时候出错了')
            return await self.finish(content)


# 用户管理所有信息展示
class GetSysUserListHandler(GetUserHandler):
    async def get(self):
        page = self.get_argument('page', '1')
        limit = self.get_argument('limit', '10')
        key = self.get_argument('keyWord', '')
        try:
            page_int = int(page)
            limit_int = int(limit)
            values = await self.application.objects.execute(SysUser.select().where(SysUser.user_name.contains(key)).paginate(page_int, limit_int))
            count = await self.application.objects.count(SysUser.select().where(SysUser.user_name.contains(key)))
            data_list = []
            for value in values:
                children = []
                value_dict = model_to_dict(value)
                if value.last_login_time:
                    value_dict["lastLoginTimeStr"] = value.last_login_time.strftime("%Y-%m-%d %H:%M:%S")
                childs = await self.application.objects.execute(SysRole.select().join(SysUserRole, on=(SysRole.id == SysUserRole.role_id)).where(SysUserRole.user_id == value.id))
                for child in childs:
                    children.append(model_to_dict(child))
                value_dict["roleList"] = children
                data_list.append(value_dict)
            content = data(data=data_list, kwargs={"count": count})
            return await self.finish(content)
        except Exception as e:
            content = params_error(message='参数传递有误，请重试！')
            return await self.finish(content)


# 添加用户管理
class CreateConfigSysUserHandler(CheckTokenHandler):
    async def post(self):
        user_name = self.get_argument('userName', None)
        nick_name = self.get_argument('nickName', None)
        role_id = self.get_argument('roleId', None)
        password = self.get_argument('password', None)
        repassword = self.get_argument('repassword', None)
        role_list_str = self.get_argument('roleListStr', '').split(',')
        if len(password) < 6 or password != repassword:
            content = params_error(message='密码输入有误，请重试！')
            return await self.finish(content)
        hl = hashlib.md5()
        hl.update(password.encode(encoding='utf-8'))
        password = hl.hexdigest()
        try:
            value = await self.application.objects.create(SysUser, user_name=user_name, nick_name=nick_name, password=password)
            for id in role_list_str:
                await self.application.objects.create(SysUserRole, user_id=value.id, role_id=id)
            await log(self, '添加用户管理')
            content = result(message="添加成功")
            return await self.finish(content)
        except Exception as e:
            content = params_error(message='参数传递有误，请重试！')
            return await self.finish(content)


# 删除用户管理
class DeleteConfigSysUserHandler(CheckTokenHandler):
    async def post(self):
        id = self.get_argument('userId', None)
        try:
            await self.application.objects.execute(SysUserRole.delete().where(SysUserRole.user_id == id))
            await self.application.objects.execute(SysUser.delete().where(SysUser.id == id))
            await log(self, '删除用户管理')
            content = result(message='删除成功')
            return await self.finish(content)
        except Exception as e:
            content = params_error(message='查找菜单管理的时候出错了')
            return await self.finish(content)


# 修改用户管理
class UpdateConfigSysUserHandler(CheckTokenHandler):
    async def post(self):
        id = self.get_argument('id', None)
        rid = self.get_argument('rId', None)
        user_name = self.get_argument('userName', None)
        nick_name = self.get_argument('nickName', None)
        password = self.get_argument('password', None)
        repassword = self.get_argument('repassword', None)
        role_id = self.get_argument('roleId', '')
        role_list_str = self.get_argument('roleListStr', '').split(',')
        if len(password) < 6 or password != repassword:
            content = params_error(message='密码输入有误，请重试！')
            return await self.finish(content)
        hl = hashlib.md5()
        hl.update(password.encode(encoding='utf-8'))
        password = hl.hexdigest()
        try:
            await self.application.objects.execute(SysUser.update(user_name=user_name, nick_name=nick_name, password=password).where(SysUser.id == id))
            await self.application.objects.execute(SysUserRole.delete().where(SysUserRole.user_id == id))
            for role_id in role_list_str:
                await self.application.objects.create(SysUserRole, user_id=id, role_id=role_id)
            await log(self, '修改用户管理')
            content = result(message="更改成功")
            return await self.finish(content)
        except Exception as e:
            content = params_error(message='更改的时候出错了')
            return await self.finish(content)
