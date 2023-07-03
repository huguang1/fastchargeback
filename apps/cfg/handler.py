#!/usr/bin/pyhton
# -*- coding: utf-8 -*-
# @Author: xiaoli
# @Time: 2019/5/25
from playhouse.shortcuts import model_to_dict
from apps.pay.models import TPayInfo
from .models import TGroup, TCustomerUser
import json
from utils.restful import result, params_error, server_error, data
from base.handler import GetUserHandler, CheckTokenHandler
from config import BASE_DIR
import os
import datetime
from openpyxl import load_workbook
from utils.inserlog import log


# 会员分级所有信息展示
class GetConfigGroupListHandler(GetUserHandler):
    async def get(self):
        page = self.get_argument('page', '1')
        limit = self.get_argument('limit', '10')
        try:
            page_int = int(page)
            limit_int = int(limit)
            values = await self.application.objects.execute(TGroup.select().paginate(page_int, limit_int))
            count = await self.application.objects.count(TGroup.select())
            data_dict = []
            for value in values:
                value_dict = {
                    "id": value.id,
                    "name": value.name
                }
                if value.str_values:
                    value.str_values = json.loads(value.str_values)
                    for key, dic in value.str_values.items():
                        value_dict[key] = dic.split('&')[1]
                data_dict.append(value_dict)
            content = data(data=data_dict, kwargs={"count": count})
            return await self.finish(content)
        except Exception as e:
            content = server_error(message="查找会员分级所有信息失败，请重试")
            return await self.finish(content)


# 添加会员分级
class CreateConfigGroupSaveHandler(CheckTokenHandler):
    async def post(self):
        name = self.get_argument('name', None)
        try:
            if await self.application.objects.create(TGroup, name=name):
                await log(self, '添加会员分级')
                content = result(message="添加成功")
                return await self.finish(content)
            else:
                content = params_error(message="添加失败，请重试！")
                return await self.finish(content)
        except Exception as e:
            content = params_error(message='参数传递有误，请重试！')
            return await self.finish(content)


# 删除会员分级
class DeleteConfigGroupDelHandler(CheckTokenHandler):
    async def post(self):
        id = self.get_argument('id', None)
        try:
            if await self.application.objects.execute(TGroup.delete().where(TGroup.id == id)):
                await log(self, '删除会员分级')
                content = result(message='删除成功')
                return await self.finish(content)
            else:
                content = params_error(message='这个字典不存在')
                return await self.finish(content)
        except Exception as e:
            content = params_error(message='查找二维码的时候出错了')
            return await self.finish(content)


# 查询某个会员分级信息
class GetConfigGroupFindHandler(GetUserHandler):
    async def get(self):
        id = self.get_argument('id', '')
        try:
            value = await self.application.objects.get(TGroup, id=id)
            group = {
                "id": value.id,
                "name": value.name
            }
            if value.str_values:
                value.str_values = json.loads(value.str_values)
                for key, dic in value.str_values.items():
                    group[key] = dic
            values = await self.application.objects.execute(TPayInfo.select())
            availablePayInfo = [model_to_dict(value) for value in values]
            data_dict = {
                'group': group,
                'availablePayInfo': availablePayInfo
            }
            content = data(data=data_dict)
            return await self.finish(content)
        except Exception as e:
            content = server_error(message="查找会员分级所有信息失败，请重试")
            return await self.finish(content)


# 修改会员分级信息
class UpdateConfigGroupUpdHandler(CheckTokenHandler):
    async def post(self):
        id = self.get_argument('id', None)
        name = self.get_argument('name', None)
        str_list = self.get_argument('strValues', '').split(',')
        str_values = {}
        for str_value in str_list:
            str_values[str_value.split('&')[0]] = str_value
        str_values = json.dumps(str_values)
        try:
            if await self.application.objects.execute(TGroup.update(name=name, str_values=str_values).where(TGroup.id == id)):
                await log(self, '修改会员分级信息')
                content = result(message='更改成功')
                return await self.finish(content)
            else:
                content = params_error(message="修改失败，请重试！")
                return await self.finish(content)
        except Exception as e:
            content = params_error(message='参数传递有误，请重试！')
            return await self.finish(content)


# 会员列表所有信息展示
class GetConfigCustomerListHandler(GetUserHandler):
    async def get(self):
        page = self.get_argument('page', '1')
        limit = self.get_argument('limit', '10')
        group_id = self.get_argument('groupId', '')
        user_account = self.get_argument('userAccount', '')
        try:
            page_int = int(page)
            limit_int = int(limit)
            if group_id == '':
                values = await self.application.objects.execute(TGroup.select(TGroup.name, TCustomerUser).join(TCustomerUser,on=(TGroup.id == TCustomerUser.group_id)).where(TCustomerUser.user_account.contains(user_account), TGroup.id).paginate(page_int, limit_int))
                count = await self.application.objects.count(TGroup.select(TGroup.name, TCustomerUser).join(TCustomerUser,on=(TGroup.id == TCustomerUser.group_id)).where(TCustomerUser.user_account.contains(user_account), TGroup.id))
            else:
                values = await self.application.objects.execute(TGroup.select(TGroup.name, TCustomerUser).join(TCustomerUser, on=(TGroup.id == TCustomerUser.group_id)).where(TCustomerUser.user_account.contains(user_account), TGroup.id==group_id).paginate(page_int, limit_int))
                count = await self.application.objects.count(TGroup.select(TGroup.name, TCustomerUser).join(TCustomerUser, on=(TGroup.id == TCustomerUser.group_id)).where(TCustomerUser.user_account.contains(user_account), TGroup.id==group_id))
            data_dict = []
            for value in values:
                data_dict.append({
                    "amounts": value.id.amounts,
                    "createTime": value.id.create_time,
                    "groupId": value.id.group_id,
                    "groupName": value.name,
                    "id": value.id.id,
                    "level": value.id.level,
                    "remark": value.id.remark,
                    "updateTime": value.id.update_time,
                    "userAccount": value.id.user_account
                })
            content = data(data=data_dict, kwargs={"count": count})
            return await self.finish(content)
        except Exception as e:
            content = server_error(message="查找会员列表所有信息失败，请重试")
            return await self.finish(content)


# 获取会员分级的种类
class GetConfigGroupBoxHandler(GetUserHandler):
    async def get(self):
        try:
            values = await self.application.objects.execute(TGroup.select(TGroup.id, TGroup.name))
            count = len(values)
            content = data(data=[model_to_dict(value) for value in values], kwargs={"count": count})
            return await self.finish(content)
        except Exception as e:
            content = server_error(message="查找会员分级所有信息失败，请重试")
            return await self.finish(content)


# 添加会员账号，并修改会员账号
class CreateConfigCustomerSaveHandler(CheckTokenHandler):
    async def post(self):
        id = self.get_argument('id', None)
        user_account = self.get_argument('userAccount', None)
        group_id = self.get_argument('groupId', None)
        try:
            if id:
                if await self.application.objects.execute(TCustomerUser.update(user_account=user_account, group_id=group_id).where(TCustomerUser.id==id)):
                    await log(self, '修改会员账号')
                    content = result(message="修改成功")
                    return await self.finish(content)
                else:
                    content = params_error(message="修改失败，请重试！")
                    return await self.finish(content)
            else:
                if await self.application.objects.create(TCustomerUser, user_account=user_account, group_id=group_id):
                    await log(self, '添加会员账号')
                    content = result(message="添加成功")
                    return await self.finish(content)
                else:
                    content = params_error(message="添加失败，请重试！")
                    return await self.finish(content)
        except Exception as e:
            content = params_error(message='参数传递有误，请重试！')
            return await self.finish(content)


# 删除会员
class DeleteConfigCustomerDelHandler(CheckTokenHandler):
    async def post(self):
        id = self.get_argument('id', None)
        try:
            if await self.application.objects.execute(TCustomerUser.delete().where(TCustomerUser.id == id)):
                await log(self, '删除会员')
                content = result(message='删除成功')
                return await self.finish(content)
            else:
                content = params_error(message='这个字典不存在')
                return await self.finish(content)
        except Exception as e:
            content = params_error(message='查找二维码的时候出错了')
            return await self.finish(content)


# 批量删除会员
class DeleteConfigCustomerBatchDelHandler(CheckTokenHandler):
    async def post(self):
        id_list = self.get_argument('ids', '').split(',')
        try:
            if await self.application.objects.execute(TCustomerUser.delete().where(TCustomerUser.id.in_(id_list))):
                await log(self, '批量删除会员')
                content = result(message='删除成功')
                return await self.finish(content)
            else:
                content = params_error(message='这个字典不存在')
                return await self.finish(content)
        except Exception as e:
            content = params_error(message='查找二维码的时候出错了')
            return await self.finish(content)


# 会员列表下载模板
class GetConfigCustomerDownMemberTempHandler(GetUserHandler):
    async def get(self):
        filename = 'wenjian.xlsx'
        FILE = os.path.join(BASE_DIR, "Files")
        self.set_header('Content-Type', 'application/octet-stream')
        filename_chuan = datetime.datetime.now().strftime('%Y-%m-%d') + '.xlsx'
        self.set_header('Content-Disposition', 'attachment; filename=' + filename_chuan)
        file = os.path.join(FILE, filename)
        with open(file, 'rb') as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                self.write(data)
        await log(self, '会员列表下载模板')
        self.finish()


# 会员列表上传文件
class UpConfigCustomerUpdHandler(CheckTokenHandler):
    async def post(self):
        group_id = self.request.arguments.get("groupId")
        files = self.request.files['file']
        filename = files[0]['filename']
        filebody = files[0]['body']
        FILE = os.path.join(BASE_DIR, "Files")
        file_path = os.path.join(FILE, filename)
        if not group_id:
            content = params_error(message="参数传递错误，请重试！")
            return await self.finish(content)
        try:
            group_id = str(group_id[0], encoding='utf-8')
            with open(file_path, 'wb') as f:
                f.write(filebody)
            # with open(file_path) as f:
            #     f_csv = csv.reader(f)
            #     headerd = next(f_csv)
            #     for row in f_csv:
            #         print(row)
            #         if await self.application.objects.create(TCustomerUser, user_account=row[0], group_id=group_id):
            #             pass
            #         else:
            #             content = params_error(message="添加失败，请重试！")
            #             return await self.finish(content)
            # os.remove(file_path)
            wb = load_workbook(filename=file_path)
            sheets = wb.get_sheet_names()
            sheet_first = sheets[0]
            ws = wb.get_sheet_by_name(sheet_first)
            rows = ws.rows
            columns = ws.columns
            i = 1
            for row in rows:
                if i == 1:
                    i += 1
                    continue
                line = [col.value for col in row]
                if await self.application.objects.create(TCustomerUser, user_account=line[0], group_id=group_id):
                    pass
                else:
                    content = params_error(message="添加失败，请重试！")
                    return await self.finish(content)
            os.remove(file_path)
            await log(self, '会员列表上传文件')
            content = result(message="添加成功")
            return await self.finish(content)
        except Exception as e:
            content = params_error(message="添加失败，请重试！")
            return await self.finish(content)
