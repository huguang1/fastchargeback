#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author: June
# @Time : 2019/5/25
from constant import Constants
from utils.json import DecimalEncoder
from .models import TLookupItem, TPayInfo, TPayApi, TPayCode
import json
from playhouse.shortcuts import model_to_dict
from base.handler import GetUserHandler, CheckTokenHandler
from utils.restful import result, params_error, server_error, data
import base64
from utils.inserlog import log


# 支付二维码所有信息展示，同时负责查询任务
class GetConfigPayCodeViewHandler(GetUserHandler):
    async def get(self):
        page = self.get_argument('page', '1')
        limit = self.get_argument('limit', '10')
        pay_code = self.get_argument('payCode', '')
        try:
            page_int = int(page)
            limit_int = int(limit)
            values = await self.application.objects.execute(TPayCode.select().where(TPayCode.pay_code.contains(pay_code)).paginate(page_int, limit_int))
            count = await self.application.objects.count(TPayCode.select().where(TPayCode.pay_code.contains(pay_code)))
            content = data(data=[model_to_dict(value) for value in values], kwargs={"count": count})
            return await self.finish(content)
        except Exception as e:
            content = server_error(message="查找二维码所有信息失败，请重试")
            return await self.finish(content)


# 支持二维码的支付通道
class GetConfigPayCodeGetListHandler(GetUserHandler):
    async def get(self):
        try:
            values = await self.application.objects.execute(TPayInfo.select().where(TPayInfo.payment_code == 'erweima'))
            content = data(data=[model_to_dict(i) for i in values])
            await self.finish(content)
        except Exception as e:
            content = server_error(message="查找支持二维码支付通道失败，请重试")
            return await self.finish(content)


# 添加二维码
class CreateConfigPayCodeFileUploadHandler(CheckTokenHandler):
    async def post(self):
        payType = self.get_argument('payType', None)
        comment = self.get_argument('comment', None)
        files = self.request.files
        comment = files['file'][0]['filename']
        body = files['file'][0]['body']
        body = "data:image/png;base64," + str(base64.b64encode(body), encoding='utf-8')
        try:
            if await self.application.objects.create(TPayCode, code=body, comment=comment, pay_code=payType):
                await log(self, '添加二维码')
                content = result(message="添加成功")
                return await self.finish(content)
            else:
                content = params_error(message="添加失败，请重试！")
                return await self.finish(content)
        except Exception as e:
            content = params_error(message='参数传递有误，请重试！')
            return await self.finish(content)


# 删除二维码
class DeleteConfigPayCodeHandler(CheckTokenHandler):
    async def post(self):
        id = self.get_argument('id', None)
        try:
            if await self.application.objects.execute(TPayCode.delete().where(TPayCode.id == id)):
                await log(self, '删除二维码')
                content = result(message='删除成功')
                return await self.finish(content)
            else:
                content = params_error(message='这个字典不存在')
                return await self.finish(content)
        except Exception as e:
            content = params_error(message='查找二维码的时候出错了')
            return await self.finish(content)


# 更改二维码
class UpdateConfigPayCodeStatusHandler(CheckTokenHandler):
    async def post(self):
        id = self.get_argument('id', None)
        status = self.get_argument('status', None)
        try:
            if await self.application.objects.execute(TPayCode.update(status=status).where(TPayCode.id == id)):
                await log(self, '更改二维码')
                content = result(message='更改成功')
                return await self.finish(content)
            else:
                content = params_error(message="修改失败，请重试！")
                return await self.finish(content)
        except Exception as e:
            content = params_error(message='参数传递有误，请重试！')
            return await self.finish(content)


# 支付类型所有信息展示
class GetLookUpItemByGroupCodePageHandler(GetUserHandler):
    async def get(self):
        groupCode = self.get_argument('groupCode', '')
        page = self.get_argument('page', '1')
        limit = self.get_argument('limit', '10')
        state = self.get_argument('state', None)
        try:
            page_int = int(page)
            limit_int = int(limit)
            if state:
                values = await self.application.objects.execute(TLookupItem.select().where(TLookupItem.group_code == groupCode,TLookupItem.state ==state))
                count = len(values)
            else:
                values = await self.application.objects.execute(TLookupItem.select().where(TLookupItem.group_code == groupCode).paginate(page_int, limit_int))
                count = await self.application.objects.count(TLookupItem.select().where(TLookupItem.group_code == groupCode))
            content = data(data=[model_to_dict(value) for value in values], kwargs={"count": count})
            return await self.finish(content)
        except Exception as e:
            content = server_error(message="查找支付类型所有信息失败，请重试")
            return await self.finish(content)


# 获取某个支付类型信息
class GetLookUpItemByGroupCodeHandler(GetUserHandler):
    async def get(self):
        groupCode = self.get_argument('groupCode', None)
        try:
            values = await self.application.objects.execute(TLookupItem.select().where(TLookupItem.group_code == groupCode))
            count = len(values)
            content = data(data=[model_to_dict(value) for value in values], kwargs={"count": count})
            return await self.finish(content)
        except Exception as e:
            content = server_error(message="查找支付类型所有信息失败，请重试")
            return await self.finish(content)


# 增加支付类型，修改支付类型
class CreateConfigLookUpItemSaveHandler(CheckTokenHandler):
    async def post(self):
        attribute_1 = self.get_argument('attribute1', None)
        attribute_2 = self.get_argument('attribute2', None)
        attribute_3 = self.get_argument('attribute3', None)
        attribute_4 = self.get_argument('attribute4', None)
        attribute_5 = self.get_argument('attribute5', None)
        group_code = self.get_argument('groupCode', None)
        id = self.get_argument('id', '')
        item_code = self.get_argument('itemCode', None)
        item_name = self.get_argument('itemName', None)
        sort = self.get_argument('sort', None)
        state = self.get_argument('state', None)
        try:
            if id == '':
                if await self.application.objects.create(TLookupItem,attribute_1=attribute_1,attribute_2=attribute_2,attribute_3=attribute_3,attribute_4=attribute_4,attribute_5=attribute_5,group_code=group_code,item_code=item_code,item_name=item_name,sort=sort,state=state):
                    await log(self, '增加支付类型')
                    content = result(message="添加成功")
                    return await self.finish(content)
                else:
                    content = params_error(message="添加失败，请重试！")
                    return await self.finish(content)
            else:
                if await self.application.objects.execute(TLookupItem.update(attribute_1=attribute_1,attribute_2=attribute_2,attribute_3=attribute_3,attribute_4=attribute_4,attribute_5=attribute_5,group_code=group_code,item_code=item_code,item_name=item_name,sort=sort,state=state).where(TLookupItem.id == id)):
                    await log(self, '更改支付类型')
                    content = result(message='更改成功')
                    return await self.finish(content)
                else:
                    content = params_error(message="修改失败，请重试！")
                    return await self.finish(content)
        except Exception as e:
            content = params_error(message='参数传递有误，请重试！')
            return await self.finish(content)


# 删除支付类型
class DeleteConfigLookUpItemHandler(CheckTokenHandler):
    async def post(self):
        id = self.get_argument('id', None)
        try:
            if await self.application.objects.execute(TLookupItem.delete().where(TLookupItem.id == id)):
                await log(self, '删除支付类型')
                content = result(message='删除成功')
                return await self.finish(content)
            else:
                content = params_error(message='这个字典不存在')
                return await self.finish(content)
        except Exception as e:
            content = params_error(message='查找支付类型的时候出错了')
            return await self.finish(content)


# 获取到某个支付类型的所有信息
class GetConfigLookUpItemInfoHandler(GetUserHandler):
    async def get(self):
        id = self.get_argument('id', '')
        try:
            value = await self.application.objects.get(TLookupItem, id=id)
            data_dict = {
                'id': value.id,
                'itemCode': value.item_code,
                'itemName': value.item_name,
                'sort': value.sort,
                'state': value.state,
                'groupCode': value.group_code,
                'parentItemCode': value.parent_item_code,
                'attribute1': value.attribute_1,
                'attribute2': value.attribute_2,
                'attribute3': value.attribute_3,
                'attribute4': value.attribute_4,
                'attribute5': value.attribute_5,
                "createUser": value.create_user,
                "createTime": value.create_time,
                "updateUser": value.update_user,
                "udpateTime": value.udpate_time
            }
            content = data(data=data_dict)
            return await self.finish(content)
        except Exception as e:
            content = server_error(message="查找支付类型信息失败，请重试")
            return await self.finish(content)


# 支付平台所有信息展示
class GetConfigPayApiListHandler(GetUserHandler):
    async def get(self):
        page = self.get_argument('page', None)
        limit = self.get_argument('limit', None)
        paymentCode = self.get_argument('paymentCode', '')
        try:
            if page is not None and limit is not None:
                if page == '' or limit == '':
                    page_int = 1
                    limit_int = 10
                page_int = int(page)
                limit_int = int(limit)
                values = await self.application.objects.execute(TPayApi.select().where(TPayApi.payment_code.contains(paymentCode) | TPayApi.payment_name.contains(paymentCode)).paginate(page_int, limit_int))
                count = await self.application.objects.count(TPayApi.select().where(TPayApi.payment_code.contains(paymentCode) | TPayApi.payment_name.contains(paymentCode)))
            else:
                values = await self.application.objects.execute(TPayApi.select())
                count = len(values)
            content = data(data=[model_to_dict(value) for value in values], kwargs={"count": count})
            return await self.finish(content)
        except Exception as e:
            content = server_error(message="查找支付平台所有信息失败，请重试")
            return await self.finish(content)


# 增加支付平台，同时负责更改支付平台
class CreateConfigPayApiSaveHandler(CheckTokenHandler):
    async def post(self):
        api_key = self.get_argument('apiKey', None)
        attribute_1 = self.get_argument('attribute1', None)
        attribute_2 = self.get_argument('attribute2', None)
        attribute_3 = self.get_argument('attribute3', None)
        attribute_4 = self.get_argument('attribute4', None)
        attribute_5 = self.get_argument('attribute5', None)
        callback_url = self.get_argument('callbackUrl', None)
        http_type = self.get_argument('httpType', None)
        http_url = self.get_argument('httpUrl', None)
        id = self.get_argument('id', '')
        memberid = self.get_argument('memberid', None)
        notify_type = self.get_argument('notifyType', None)
        notify_url = self.get_argument('notifyUrl', None)
        param_format = self.get_argument('paramFormat', None)
        payment_code = self.get_argument('paymentCode', None)
        payment_name = self.get_argument('paymentName', None)
        query_url = self.get_argument('queryUrl', None)
        remark = self.get_argument('remark', None)
        sign_format = self.get_argument('signFormat', None)
        sign_type = self.get_argument('signType', None)
        state = self.get_argument('state', None)
        verify_format = self.get_argument('verifyFormat', None)

        try:
            if id == '':
                if await self.application.objects.create(TPayApi,api_key=api_key,attribute_1=attribute_1,attribute_2=attribute_2,attribute_3=attribute_3,attribute_4=attribute_4,
                                                         attribute_5=attribute_5,callback_url=callback_url,http_type=http_type,http_url=http_url,memberid=memberid,
                                                         notify_type=notify_type,notify_url=notify_url,param_format=param_format, payment_code=payment_code, payment_name=payment_name,
                                                         query_url=query_url, remark=remark,sign_format=sign_format, sign_type=sign_type,state=state,verify_format=verify_format):
                    await log(self, '增加支付平台')
                    content = result(message="添加成功")
                    return await self.finish(content)
                else:
                    content = params_error(message="添加失败，请重试！")
                    return await self.finish(content)
            else:
                if await self.application.objects.execute(TPayApi.update(api_key=api_key,attribute_1=attribute_1,attribute_2=attribute_2,attribute_3=attribute_3,attribute_4=attribute_4,
                                                         attribute_5=attribute_5,callback_url=callback_url,http_type=http_type,http_url=http_url,memberid=memberid,
                                                         notify_type=notify_type,notify_url=notify_url,param_format=param_format, payment_code=payment_code, payment_name=payment_name,
                                                         query_url=query_url, remark=remark,sign_format=sign_format, sign_type=sign_type,state=state,verify_format=verify_format).where(TPayApi.id == id)):
                    await log(self, '更改支付平台')
                    content = result(message='更改成功')
                    return await self.finish(content)
                else:
                    content = params_error(message="修改失败，请重试！")
                    return await self.finish(content)
        except Exception as e:
            content = params_error(message='参数传递有误，请重试！')
            return await self.finish(content)


# 删除支付平台
class DeleteConfigPayApiByIdHandler(CheckTokenHandler):
    async def post(self):
        id = self.get_argument('id', None)
        try:
            if await self.application.objects.execute(TPayApi.delete().where(TPayApi.id == id)):
                await log(self, '删除支付平台')
                content = result(message='删除成功')
                return await self.finish(content)
            else:
                content = params_error(message='这个字典不存在')
                return await self.finish(content)
        except Exception as e:
            content = params_error(message='查找支付类型的时候出错了')
            return await self.finish(content)


# 获取某个支付平台的详细信息
class GetConfigPayApiInfoHandler(GetUserHandler):
    async def get(self):
        id = self.get_argument('id', '')
        try:
            value = await self.application.objects.get(TPayApi, id=id)
            data_dict = {
                    "id": value.id,
                    "paymentCode": value.payment_code,
                    "paymentName": value.payment_name,
                    "state": value.state,
                    "memberid": value.memberid,
                    "apiKey": value.api_key,
                    "httpUrl": value.http_url,
                    "httpType": value.http_type,
                    "notifyUrl": value.notify_url,
                    "notifyType": value.notify_type,
                    "callbackUrl": value.callback_url,
                    "queryUrl": value.query_url,
                    "signType": value.sign_type,
                    "signFormat": value.sign_format,
                    "paramFormat": value.param_format,
                    "verifyFormat": value.verify_format,
                    "remark": value.remark,
                    "attribute1": value.attribute_1,
                    "attribute2": value.attribute_2,
                    "attribute3": value.attribute_3,
                    "attribute4": value.attribute_4,
                    "attribute5": value.attribute_5,
                    "createUser": value.create_user,
                    "createTime": value.create_time,
                    "updateUser": value.update_user,
                    "udpateTime": value.udpate_time
                }
            content = data(data=data_dict)
            return await self.finish(content)
        except Exception as e:
            content = server_error(message="查找支付类型信息失败，请重试")
            return await self.finish(content)


# 支付通道所有信息展示，同时负责查询任务
class GetConfigPayInfoAllHandler(GetUserHandler):
    async def get(self):
        page = self.get_argument('page', '1')
        limit = self.get_argument('limit', '10')
        payment_code = self.get_argument('paymentCode', '')
        item_code = self.get_argument('itemCode', '')
        try:
            page_int = int(page)
            limit_int = int(limit)
            values = await self.application.objects.execute(TPayInfo.select().where(TPayInfo.payment_code.contains(payment_code) & TPayInfo.item_code.contains(item_code)).paginate(page_int, limit_int))
            count = await self.application.objects.count(TPayInfo.select().where(TPayInfo.payment_code.contains(payment_code) & TPayInfo.item_code.contains(item_code)))
            content = data(data=[model_to_dict(value) for value in values], kwargs={"count": count})
            return await self.finish(content)
        except Exception as e:
            content = server_error(message="查找支付类型所有信息失败，请重试")
            return await self.finish(content)


# 添加支付通道
class CreateConfigPayInfoSaveHandler(CheckTokenHandler):
    async def post(self):
        bank_code = self.get_argument('bankCode', None)
        id = self.get_argument('id', '')
        item_code = self.get_argument('itemCode', '')
        max_amount = self.get_argument('maxAmount', None)
        max_switch = self.get_argument('maxSwitch', None)
        min_amount = self.get_argument('minAmount', None)
        min_switch = self.get_argument('minSwitch', None)
        pay_code = self.get_argument('payCode', None)
        payment_code = self.get_argument('paymentCode', '')
        point_switch = self.get_argument('pointSwitch', None)
        rate = self.get_argument('rate', None)
        rate_type = self.get_argument('rateType', None)
        state = self.get_argument('state', None)
        wangyinType = self.get_argument('wangyinType', None)
        try:
            lookup = await self.application.objects.get(TLookupItem, item_code=item_code)
            if lookup.attribute_1 == 'PC':
                pay_model = 1
            elif lookup.attribute_1 == 'WAP':
                pay_model = 2
            elif lookup.attribute_1 == '网银内部':
                pay_model = 3
            elif lookup.attribute_1 == '网银外部':
                pay_model = 4
            else:
                pay_model = 0
            item_name = lookup.item_name
            icon = lookup.attribute_4
            payapi = await self.application.objects.get(TPayApi, payment_code=payment_code)
            payment_name = payapi.payment_name
            if id == '':
                if await self.application.objects.create(TPayInfo, bank_code=bank_code, item_code=item_code, max_amount=max_amount, max_switch=max_switch, min_amount=min_amount,
                                                         min_switch=min_switch, pay_code=pay_code, payment_code=payment_code, point_switch=point_switch, rate=rate,
                                                         rate_type=rate_type, state=state, pay_model=pay_model, item_name=item_name, icon=icon, payment_name=payment_name):
                    await log(self, '添加支付通道')
                    content = result(message="添加成功")
                    return await self.finish(content)
                else:
                    content = params_error(message="添加失败，请重试！")
                    return await self.finish(content)
            else:
                if await self.application.objects.execute(TPayInfo.update(bank_code=bank_code, item_code=item_code, max_amount=max_amount, max_switch=max_switch, min_amount=min_amount,
                                                         min_switch=min_switch, pay_code=pay_code, payment_code=payment_code, point_switch=point_switch, rate=rate,
                                                         rate_type=rate_type, state=state, pay_model=pay_model, item_name=item_name, icon=icon, payment_name=payment_name).where(TPayInfo.id == id)):
                    await log(self, '更改支付通道')
                    content = result(message='更改成功')
                    return await self.finish(content)
                else:
                    content = params_error(message="修改失败，请重试！")
                    return await self.finish(content)
        except Exception as e:
            content = params_error(message='参数传递有误，请重试！')
            return await self.finish(content)


# 删除支付通道
class DeleteConfigPayInfoHandler(CheckTokenHandler):
    async def post(self):
        id = self.get_argument('id', None)
        try:
            if await self.application.objects.execute(TPayInfo.delete().where(TPayInfo.id == id)):
                await log(self, '删除支付通道')
                content = result(message='删除成功')
                return await self.finish(content)
            else:
                content = params_error(message='这个字典不存在')
                return await self.finish(content)
        except Exception as e:
            content = params_error(message='查找支付类型的时候出错了')
            return await self.finish(content)


# 获取某个支付通道的信息
class GetConfigPayInfoInfoHandler(GetUserHandler):
    async def get(self):
        id = self.get_argument('id', '')
        try:
            value = await self.application.objects.get(TPayInfo, id=id)
            data_dict = {
                "id": value.id,
                "paymentCode": value.payment_code,
                "paymentName": value.payment_name,
                "payCode": value.pay_code,
                "itemName": value.item_name,
                "itemCode": value.item_code,
                "payModel": value.pay_model,
                "icon": value.icon,
                "rate": value.rate,
                "rateType": value.rate_type,
                "state": value.state,
                "minSwitch": value.min_switch,
                "maxSwitch": value.max_switch,
                "minAmount": value.min_amount,
                "maxAmount": value.max_amount,
                "pointSwitch": value.point_switch,
                "wangyinType": None,
                "bankCode": value.bank_code,
                "createUser": value.create_user,
                "createTime": value.create_time,
                "updateUser": value.update_user,
                "udpateTime": value.udpate_time
            }
            content = data(data=data_dict)
            return await self.finish(content)
        except Exception as e:
            content = server_error(message="查找支付类型信息失败，请重试")
            return await self.finish(content)
