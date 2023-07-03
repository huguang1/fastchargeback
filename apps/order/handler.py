#!/usr/bin/pyhton
# -*- coding: utf-8 -*-
# @Author: xiaoli
# @Time: 2019/5/25
import datetime
from playhouse.shortcuts import model_to_dict, fn
from utils.restful import result, params_error, server_error, data
from base.handler import GetUserHandler, CheckTokenHandler
from .models import TOrderHis, TOrder, TOrderDaliySum
from apps.pay.models import TPayInfo
import csv
from config import BASE_DIR
import os
from utils.inserlog import log


# 所有历史订单展示，同时负责查询任务
class GetConfigOrderListOrderHisHandler(GetUserHandler):
    async def get(self):
        page = self.get_argument('page', '1')
        limit = self.get_argument('limit', '10')
        start_time = self.get_argument('startTime', '')
        end_time = self.get_argument('endTime', '')
        order_state = self.get_argument('orderState', '')
        key = self.get_argument('key', '')  # 用户名，订单编号，操作人
        if order_state == '':
            order_state = 30
        try:
            page_int = int(page)
            limit_int = int(limit)
            end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S") if end_time else datetime.datetime.now()
            start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S") if start_time else datetime.datetime.strptime("1971-01-01 18:55:23", "%Y-%m-%d %H:%M:%S")
            values = await self.application.objects.execute(TOrderHis.select(TOrderHis, TPayInfo.payment_name, TPayInfo.item_name).join(TPayInfo, on=(TOrderHis.payment_code == TPayInfo.payment_code)).where(TOrderHis.pay_code == TPayInfo.pay_code,TOrderHis.user_account.contains(key) | TOrderHis.order_id.contains(key) | TOrderHis.update_user.contains(key), TOrderHis.order_state == order_state, TOrderHis.order_time >= start_time, TOrderHis.order_time <= end_time).paginate(page_int, limit_int))
            sums = await self.application.objects.execute(TOrderHis.select(fn.SUM(TOrderHis.order_amount), fn.SUM(TOrderHis.rate_amount),fn.Count(TOrderHis.id)).join(TPayInfo, on=(TOrderHis.payment_code == TPayInfo.payment_code)).where(TOrderHis.pay_code == TPayInfo.pay_code,TOrderHis.user_account.contains(key) | TOrderHis.order_id.contains(key) | TOrderHis.update_user.contains(key),TOrderHis.order_state == order_state,TOrderHis.order_time <= end_time))
            data_list = []
            count = 0
            responseData = {}
            for a in sums:
                responseData["allMoney"] = a.order_amount
                responseData["allPoundage"] = a.rate_amount
                count = a.id
            for value in values:
                data_list.append({
                    "itemCode": value.item_code,
                    "lockId": value.lock_id,
                    # "operationTime": value.operationTime,
                    "orderAmount": value.order_amount,
                    "orderDesc": value.order_desc,
                    # "orderFrom": value.orderFrom,  #
                    "orderId": value.order_id,
                    # "orderMoneyStr": value.orderMoneyStr,  #
                    "orderState": value.order_state,
                    # "orderStateStr": value.orderStateStr,  #
                    "orderTime": value.order_time,
                    # "orderTimeStr": value.orderTimeStr,  #
                    "payCode": value.pay_code,
                    "payName": value.payment_code.item_name,
                    "payOrder": value.pay_order,
                    # "paymentCode": value.payment_code,
                    "paymentName": value.payment_code.payment_name,
                    "rate": value.rate,
                    "rateAmount": value.rate_amount,
                    "state": value.state,
                    # "stateStr": value.stateStr,  #
                    "updateTime": value.update_time,
                    "updateUser": value.update_user,
                    "userAccount": value.user_account,
                    # "userId": value.userId,
                    "userIp": value.user_ip,
                })
            content = data(data=data_list, kwargs={"count": count, "responseData": responseData})
            return await self.finish(content)
        except Exception as e:
            print(e)
            content = params_error(message='参数传递有误，请重试！')
            return await self.finish(content)


# 所有订单列表展示，同时负责查询任务
class GetConfigOrderGridHandler(GetUserHandler):
    async def get(self):
        page = self.get_argument('page', '1')
        limit = self.get_argument('limit', '10')
        start_time = self.get_argument('startTime', '')
        end_time = self.get_argument('endTime', '')
        key = self.get_argument('key', '')  # 用户名，订单编号，操作人
        order_state = self.get_argument('orderState', '')
        payment_code = self.get_argument('paymentCode', '')  # 平台名称
        try:
            page_int = int(page)
            limit_int = int(limit)
            end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S") if end_time else datetime.datetime.now()
            start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S") if start_time else datetime.datetime.strptime("1971-01-01 18:55:23", "%Y-%m-%d %H:%M:%S")
            if order_state == '':
                values = await self.application.objects.execute(TOrder.select(TOrder, TPayInfo.payment_name, TPayInfo.item_name).join(TPayInfo, on=(TOrder.payment_code == TPayInfo.payment_code)).where(TOrder.pay_code == TPayInfo.pay_code,TOrder.user_account.contains(key) | TOrder.order_id.contains(key) | TOrder.update_user.contains(key), TOrder.order_time >= start_time, TOrder.order_time <= end_time, TOrder.payment_code.startswith(payment_code)).paginate(page_int, limit_int))
                sums = await self.application.objects.execute(TOrder.select(fn.Count(TOrder.id)).join(TPayInfo, on=(TOrder.payment_code == TPayInfo.payment_code)).where(TOrder.pay_code == TPayInfo.pay_code,TOrder.user_account.contains(key) | TOrder.order_id.contains(key) | TOrder.update_user.contains(key),TOrder.order_time >= start_time, TOrder.order_time <= end_time, TOrder.payment_code.startswith(payment_code)))
            else:
                values = await self.application.objects.execute(TOrder.select(TOrder, TPayInfo.payment_name, TPayInfo.item_name).join(TPayInfo, on=(TOrder.payment_code == TPayInfo.payment_code)).where(TOrder.pay_code == TPayInfo.pay_code,TOrder.user_account.contains(key) | TOrder.order_id.contains(key) | TOrder.update_user.contains(key),TOrder.order_state == order_state,TOrder.order_time >= start_time,TOrder.order_time <= end_time,TOrder.payment_code.startswith(payment_code)).paginate(page_int,limit_int))
                sums = await self.application.objects.execute(TOrder.select(fn.Count(TOrder.id)).join(TPayInfo, on=(TOrder.payment_code == TPayInfo.payment_code)).where(TOrder.pay_code == TPayInfo.pay_code,TOrder.user_account.contains(key) | TOrder.order_id.contains(key) | TOrder.update_user.contains(key),TOrder.order_state == order_state,TOrder.order_time >= start_time,TOrder.order_time <= end_time,TOrder.payment_code.startswith(payment_code)))
            data_list = []
            count = 0
            for a in sums:
                count = a.id
            for value in values:
                data_list.append({
                    "id": value.id,
                    "itemCode": value.item_code,
                    "lockId": value.lock_id,
                    # "operationTime": value.operationTime,
                    "orderAmount": value.order_amount,
                    "orderDesc": value.order_desc,
                    # "orderFrom": value.orderFrom,
                    "orderId": value.order_id,
                    # "orderMoneyStr": value.orderMoneyStr,
                    "orderState": value.order_state,
                    # "orderStateStr": value.orderStateStr,
                    "orderTime": value.order_time,
                    # "orderTimeStr": value.orderTimeStr,
                    "payCode": value.pay_code,
                    "payName": value.payment_code.item_name,
                    "payOrder": value.pay_order,
                    # "paymentCode": value.payment_code,
                    "paymentName": value.payment_code.payment_name,
                    "rate": value.rate,
                    "rateAmount": value.rate_amount,
                    "state": value.state,
                    # "stateStr": value.stateStr,
                    "updateTime": value.update_time,
                    "updateUser": value.update_user,
                    "userAccount": value.user_account,
                    # "userId": value.userId,
                    "userIp": value.user_ip,
                })
            content = data(data=data_list, kwargs={"count": count})
            return await self.finish(content)
        except Exception as e:
            print(e)
            content = params_error(message='参数传递有误，请重试！')
            return await self.finish(content)


# 订单列表导出excel
class GetConfigOrderGeneralExcelHandler(GetUserHandler):
    async def get(self):
        start_time = self.get_argument('startTime', '')
        end_time = self.get_argument('endTime', '')
        key = self.get_argument('key', '')  # 用户名，订单编号，操作人
        order_state = self.get_argument('orderState', '')
        payment_code = self.get_argument('paymentCode', '')  # 平台名称
        try:
            end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S") if end_time else datetime.datetime.now()
            start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S") if start_time else datetime.datetime.strptime("1971-01-01 18:55:23", "%Y-%m-%d %H:%M:%S")
            if order_state == '':
                values = await self.application.objects.execute(TOrder.select(TOrder, TPayInfo.payment_name, TPayInfo.item_name).join(TPayInfo, on=(TOrder.payment_code == TPayInfo.payment_code)).where(TOrder.pay_code == TPayInfo.pay_code,TOrder.user_account.contains(key) | TOrder.order_id.contains(key) | TOrder.update_user.contains(key), TOrder.order_time >= start_time, TOrder.order_time <= end_time, TOrder.payment_code.startswith(payment_code)))
            else:
                values = await self.application.objects.execute(TOrder.select(TOrder, TPayInfo.payment_name, TPayInfo.item_name).join(TPayInfo, on=(TOrder.payment_code == TPayInfo.payment_code)).where(TOrder.pay_code == TPayInfo.pay_code,TOrder.user_account.contains(key) | TOrder.order_id.contains(key) | TOrder.update_user.contains(key), TOrder.order_state == order_state, TOrder.order_time >= start_time, TOrder.order_time <= end_time, TOrder.payment_code.startswith(payment_code)))
            filename = datetime.datetime.now().strftime("%Y-%m-%d") + '.csv'
            FILE = os.path.join(BASE_DIR, "Files")
            file = os.path.join(FILE, filename)
            with open(file, 'w') as f:
                csv_writer = csv.writer(f, dialect='excel')
                csv_writer.writerow(['订单编码', '用户名', '支付方式', '订单金额', '订单时间', '订单来源', '订单状态', '处理状态', '备注'])
                for a in values:
                    csv_writer.writerow([a.order_id, a.user_account, a.payment_code.item_code, a.order_amount, a.update_time, a.payment_code.payment_name, a.order_state, a.state, a.order_desc])
            await log(self, '订单列表导出excel')
            content = result(message='下载成功', data=filename)
            return await self.finish(content)
        except Exception as e:
            print(e)
            content = params_error(message='参数传递有误，请重试！')
            return await self.finish(content)


# 订单列表下载文件
class GetConfigOrderDownLoadExcelHandler(GetUserHandler):
    async def get(self):
        filename = self.get_argument('fileName', None)
        FILE = os.path.join(BASE_DIR, "Files")
        self.set_header('Content-Type', 'text/csv')
        self.set_header('Content-Disposition', 'attachment; filename=' + filename)
        file = os.path.join(FILE, filename)
        with open(file, 'rb') as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                self.write(data)
        os.remove(file)
        await log(self, '订单列表下载文件')
        self.finish()


# 统计订单的总的金额，以及手续费
class GetConfigOrderOrderSumHandler(GetUserHandler):
    async def get(self):
        start_time = self.get_argument('startTime', '')
        end_time = self.get_argument('endTime', '')
        key = self.get_argument('key', '')  # 用户名，订单编号，操作人
        order_state = self.get_argument('orderState', '')
        payment_code = self.get_argument('paymentCode', '')  # 平台名称
        try:
            end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S") if end_time else datetime.datetime.now()
            start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S") if start_time else datetime.datetime.strptime("1971-01-01 18:55:23", "%Y-%m-%d %H:%M:%S")
            if order_state == '':
                sums = await self.application.objects.execute(TOrder.select(fn.SUM(TOrder.order_amount), fn.SUM(TOrder.rate_amount)).join(TPayInfo, on=(TOrder.payment_code == TPayInfo.payment_code)).where(TOrder.pay_code == TPayInfo.pay_code,TOrder.user_account.contains(key) | TOrder.order_id.contains(key) | TOrder.update_user.contains(key),TOrder.order_time >= start_time, TOrder.order_time <= end_time, TOrder.payment_code.startswith(payment_code)))
            else:
                sums = await self.application.objects.execute(TOrder.select(fn.SUM(TOrder.order_amount), fn.SUM(TOrder.rate_amount)).join(TPayInfo, on=(TOrder.payment_code == TPayInfo.payment_code)).where(TOrder.pay_code == TPayInfo.pay_code,TOrder.user_account.contains(key) | TOrder.order_id.contains(key) | TOrder.update_user.contains(key),TOrder.order_state == order_state,TOrder.order_time >= start_time,TOrder.order_time <= end_time,TOrder.payment_code.startswith(payment_code)))
            responseData = {}
            for a in sums:
                responseData["allMoney"] = a.order_amount if a.order_amount else 0
                responseData["allPoundage"] = a.rate_amount if a.order_amount else 0
            content = data(kwargs={"responseData": responseData})
            return await self.finish(content)
        except Exception as e:
            content = params_error(message='参数传递有误，请重试！')
            return await self.finish(content)


# 待处理订单的所有信息展示
class GetConfigOrderToBeGridHandler(GetUserHandler):
    """
    order_state=30,已成功支付
    state=10,待处理
    就是已经支付成功了，需要确认的订单
    """
    async def get(self):
        page = self.get_argument('page', '1')
        limit = self.get_argument('limit', '10')
        order_state = self.get_argument('orderState', '')
        key = self.get_argument('key', '')  # 用户名，订单编号，操作人
        try:
            page_int = int(page)
            limit_int = int(limit)
            values = await self.application.objects.execute(TOrder.select(TOrder, TPayInfo.payment_name, TPayInfo.item_name).join(TPayInfo, on=(TOrder.payment_code == TPayInfo.payment_code)).where(TOrder.pay_code == TPayInfo.pay_code,TOrder.user_account.contains(key) | TOrder.order_id.contains(key) | TOrder.update_user.contains(key), TOrder.order_state == order_state, TOrder.state == 10).paginate(page_int, limit_int))
            sums = await self.application.objects.execute(TOrder.select(fn.SUM(TOrder.order_amount), fn.SUM(TOrder.rate_amount),fn.Count(TOrder.id)).join(TPayInfo, on=(TOrder.payment_code == TPayInfo.payment_code)).where(TOrder.pay_code == TPayInfo.pay_code,TOrder.user_account.contains(key) | TOrder.order_id.contains(key) | TOrder.update_user.contains(key),TOrder.order_state == order_state, TOrder.state == 10))
            data_list = []
            count = 0
            responseData = {}
            for a in sums:
                responseData["allMoney"] = a.order_amount
                responseData["allPoundage"] = a.rate_amount
                count = a.id
            for value in values:
                data_list.append({
                    "itemCode": value.item_code,
                    "lockId": value.lock_id,
                    # "operationTime": value.operationTime,
                    "orderAmount": value.order_amount,
                    "orderDesc": value.order_desc,
                    # "orderFrom": value.orderFrom,
                    "orderId": value.order_id,
                    # "orderMoneyStr": value.orderMoneyStr,
                    "orderState": value.order_state,
                    # "orderStateStr": value.orderStateStr,
                    "orderTime": value.order_time,
                    # "orderTimeStr": value.orderTimeStr,
                    "payCode": value.pay_code,
                    "payName": value.payment_code.item_name,
                    "payOrder": value.pay_order,
                    # "paymentCode": value.payment_code,
                    "paymentName": value.payment_code.payment_name,
                    "rate": value.rate,
                    "rateAmount": value.rate_amount,
                    "state": value.state,
                    # "stateStr": value.stateStr,
                    "updateTime": value.update_time,
                    "updateUser": value.update_user,
                    "userAccount": value.user_account,
                    # "userId": value.userId,
                    "userIp": value.user_ip,
                })
            content = data(data=data_list, kwargs={"count": count, "responseData": responseData})
            return await self.finish(content)
        except Exception as e:
            print(e)
            content = params_error(message='参数传递有误，请重试！')
            return await self.finish(content)


# 锁定，待处理订单
class LockConfigOrderLockOrderHandler(CheckTokenHandler):
    """就是将订单变成已锁定的状态"""
    async def post(self):
        order_id = self.get_argument("orderId", '')
        user = self.current_user
        try:
            value = await self.application.objects.get(TOrder, order_id=order_id)
            if await self.application.objects.execute(TOrder.update(update_user=user, update_time=datetime.datetime.now(), state=20, lock_id=user).where(TOrder.order_id == value.order_id)):
                await log(self, '锁定待处理订单')
                content = result(message="修改成功")
                return await self.finish(content)
            else:
                content = params_error(message='参数传递有误，请重试！')
                return await self.finish(content)
        except Exception as e:
            content = params_error(message='参数传递有误，请重试！')
            return await self.finish(content)


# 我的订单所有信息展示
class GetConfigOrderMyOrderHandler(GetUserHandler):
    """
    order_state=30
    state != 10
    update_user = user
    就是将所有自己操作的订单统计下来
    """
    async def get(self):
        start_time = self.get_argument('startTime', '')
        end_time = self.get_argument('endTime', '')
        page = self.get_argument('page', '1')
        limit = self.get_argument('limit', '10')
        order_state = self.get_argument('orderState', '')
        key = self.get_argument('key', '')  # 用户名，订单编号
        user = self.current_user
        if order_state == '':
            order_state = 30
        try:
            page_int = int(page)
            limit_int = int(limit)
            end_time = datetime.datetime.strptime(end_time,"%Y-%m-%d %H:%M:%S") if end_time else datetime.datetime.now()
            start_time = datetime.datetime.strptime(start_time,"%Y-%m-%d %H:%M:%S") if start_time else datetime.datetime.strptime("1971-01-01 18:55:23", "%Y-%m-%d %H:%M:%S")
            values = await self.application.objects.execute(TOrder.select(TOrder, TPayInfo.payment_name, TPayInfo.item_name).join(TPayInfo, on=(TOrder.payment_code == TPayInfo.payment_code)).where(TOrder.pay_code == TPayInfo.pay_code, TOrder.user_account.contains(key) | TOrder.order_id.contains(key), TOrder.order_state == order_state, TOrder.update_user == user, TOrder.state != 10, TOrder.update_time >= start_time, TOrder.update_time <= end_time).paginate(page_int, limit_int))
            sums = await self.application.objects.execute(TOrder.select(fn.SUM(TOrder.order_amount), fn.SUM(TOrder.rate_amount), fn.Count(TOrder.id)).join(TPayInfo, on=(TOrder.payment_code == TPayInfo.payment_code)).where(TOrder.pay_code == TPayInfo.pay_code, TOrder.user_account.contains(key) | TOrder.order_id.contains(key), TOrder.order_state == order_state, TOrder.update_user == user, TOrder.state != 10, TOrder.update_time >= start_time, TOrder.update_time <= end_time))
            data_list = []
            count = 0
            responseData = {}
            for a in sums:
                responseData["allMoney"] = a.order_amount
                responseData["allPoundage"] = a.rate_amount
                count = a.id
            for value in values:
                data_list.append({
                    "id": value.id,
                    "itemCode": value.item_code,
                    "lockId": value.lock_id,
                    # "operationTime": value.operationTime,
                    "orderAmount": value.order_amount,
                    "orderDesc": value.order_desc,
                    # "orderFrom": value.orderFrom,
                    "orderId": value.order_id,
                    # "orderMoneyStr": value.orderMoneyStr,
                    "orderState": value.order_state,
                    # "orderStateStr": value.orderStateStr,
                    "orderTime": value.order_time,
                    # "orderTimeStr": value.orderTimeStr,
                    "payCode": value.pay_code,
                    "payName": value.payment_code.item_name,
                    "payOrder": value.pay_order,
                    # "paymentCode": value.payment_code,
                    "paymentName": value.payment_code.payment_name,
                    "rate": value.rate,
                    "rateAmount": value.rate_amount,
                    "state": value.state,
                    # "stateStr": value.stateStr,
                    "updateTime": value.update_time,
                    "updateUser": value.update_user,
                    "userAccount": value.user_account,
                    # "userId": value.userId,
                    "userIp": value.user_ip,
                })
            content = data(data=data_list, kwargs={"count": count, "responseData": responseData})
            return await self.finish(content)
        except Exception as e:
            print(e)
            content = params_error(message='参数传递有误，请重试！')
            return await self.finish(content)


# 解锁，我的订单
class UpdateConfigOrderMyOrderHandler(CheckTokenHandler):
    async def post(self):
        id = self.get_argument("id", '')
        order_desc = self.get_argument('orderDesc', None)
        order_state = self.get_argument('orderState', None)
        state = self.get_argument('state', None)
        if state == '50':
            state = '10'
        try:
            value = await self.application.objects.get(TOrder, id=id)
            if await self.application.objects.execute(TOrder.update(state=state, lock_id=0).where(TOrder.id == value.id)):
                await log(self, '解锁我的订单')
                content = result(message="修改成功")
                return await self.finish(content)
            else:
                content = params_error(message='参数传递有误，请重试！')
                return await self.finish(content)
        except Exception as e:
            content = params_error(message='参数传递有误，请重试！')
            return await self.finish(content)


# 首页统计信息
class GetConfigOrderQueryIndexDataHandler(GetUserHandler):
    async def get(self):
        try:
            sums = await self.application.objects.execute(TOrder.select(fn.SUM(TOrder.order_amount), fn.Count(TOrder.id)).where(TOrder.order_state == 30))
            dailysums = await self.application.objects.execute(TOrder.select(fn.SUM(TOrder.order_amount), fn.Count(TOrder.id)).where(TOrder.order_state == 30, TOrder.update_time >= datetime.date.today()))
            allAmount = 0
            allNum = 0
            todayAmount = 0
            todayNum = 0
            for a in sums:
                allAmount = a.order_amount
                allNum = a.id
            for b in dailysums:
                todayAmount = b.order_amount
                todayNum = b.id
            content = data(kwargs={"allAmount": allAmount, "allNum": allNum, "todayAmount": todayAmount, "todayNum": todayNum})
            return await self.finish(content)
        except Exception as e:
            content = params_error(message='参数传递有误，请重试！')
            return await self.finish(content)


# 日订单金额
class GetConfigOrderQueryDaySumOrderHandler(GetUserHandler):
    async def get(self):
        pass
        # days = self.get_argument('days', None)
        # start_date = self.get_argument('startDate', None)
        # start_date = '2018-08-16'
        # try:
        #     start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        #     dailysums = await self.application.objects.execute(TOrderDaliySum.select().where(TOrderDaliySum.order_date == start_date))
        #     data_list = []
        #     a = 1
        #     # for i in range(int(days)):
        #     #     a = {"amountSuccess": 0, "amountFail": 0, "key": "2019-06-01"}
        #     #     dailysums = await self.application.objects.execute(TOrder.select(fn.SUM(TOrder.order_amount), fn.Count(TOrder.id)).where(TOrder.order_state == 30, TOrder.update_time >= start_date))
        #     #     allAmount = 0
        #     #     allNum = 0
        #     #     todayAmount = 0
        #     #     todayNum = 0
        #     #     for b in dailysums:
        #     #         todayAmount = b.order_amount
        #     #         todayNum = b.id
        #     # content = data(kwargs={"allAmount": allAmount, "allNum": allNum, "todayAmount": todayAmount, "todayNum": todayNum})
        #     # return await self.finish(content)
        # except Exception as e:
        #     content = params_error(message='参数传递有误，请重试！')
        #     return await self.finish(content)


# 周订单金额
class GetConfigOrderQueryWeekSumOrderHandler(GetUserHandler):
    async def get(self):
        weeks = self.get_argument('weeks', None)
        start_date = self.get_argument('startDate', None)
        pass


# 账目汇总
class GetConfigOrderOrderAccountsHandler(GetUserHandler):
    async def get(self):
        page = self.get_argument('page', '1')
        limit = self.get_argument('limit', '10')
        start_time = self.get_argument('startTime', None)
        end_time = self.get_argument('endTime', None)
        try:
            end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S") if end_time else datetime.datetime.now()
            start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S") if start_time else datetime.datetime.strptime("1971-01-01 18:55:23", "%Y-%m-%d %H:%M:%S")
            values = await self.application.objects.execute(TPayInfo.select(TPayInfo.payment_name, fn.SUM(TOrder.order_amount), fn.SUM(TOrder.rate_amount)).join(TOrder, on=(TPayInfo.payment_code == TOrder.payment_code)).where(TOrder.pay_code == TPayInfo.pay_code, TOrder.order_state == 30, TOrder.update_time >= start_time, TOrder.update_time <= end_time).group_by(TPayInfo.payment_name))
            data_list = []
            for value in values:
                data_list.append({
                    "pay_name": value.payment_name,
                    "amount": value.order_amount,
                    "poundage": value.rate_amount
                })
            content = data(data=data_list)
            return await self.finish(content)
        except Exception as e:
            content = params_error(message='参数传递有误，请重试！')
            return await self.finish(content)
