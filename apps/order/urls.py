#!/usr/bin/pyhton
# -*- coding: utf-8 -*-
# @Author: xiaoli
# @Time: 2019/5/25
# @Time: 2019/5/25
from tornado.web import url
from .handler import GetConfigOrderListOrderHisHandler, GetConfigOrderGridHandler, GetConfigOrderOrderSumHandler, \
    GetConfigOrderToBeGridHandler, GetConfigOrderMyOrderHandler, LockConfigOrderLockOrderHandler, \
    UpdateConfigOrderMyOrderHandler, GetConfigOrderQueryIndexDataHandler, GetConfigOrderQueryDaySumOrderHandler, \
    GetConfigOrderQueryWeekSumOrderHandler, GetConfigOrderOrderAccountsHandler, GetConfigOrderGeneralExcelHandler, \
    GetConfigOrderDownLoadExcelHandler

urlpattern = [
    url(r"/config/order/listOrderHis", GetConfigOrderListOrderHisHandler),  # 所有历史订单展示，同时负责查询任务
    url(r"/config/order/ordergrid", GetConfigOrderGridHandler),  # 所有订单列表展示，同时负责查询任务
    url(r"/config/order/orderSum", GetConfigOrderOrderSumHandler),  # 统计订单的总的金额，以及手续费
    url(r"/config/order/tobegrid", GetConfigOrderToBeGridHandler),  # 待处理订单的所有信息展示
    url(r"/config/order/myOrder", GetConfigOrderMyOrderHandler),  # 我的订单所有信息展示
    url(r"/config/order/lockOrder", LockConfigOrderLockOrderHandler),  # 锁定，待处理订单
    url(r"/config/order/updateMyOrder", UpdateConfigOrderMyOrderHandler),  # 解锁，我的订单
    url(r"/config/order/queryIndexData", GetConfigOrderQueryIndexDataHandler),  # 首页统计信息
    url(r"/config/order/queryDaySumOrder", GetConfigOrderQueryDaySumOrderHandler),  # 日订单金额
    url(r"/config/order/queryWeekSumOrder", GetConfigOrderQueryWeekSumOrderHandler),  # 周订单金额
    url(r"/config/order/orderAccounts", GetConfigOrderOrderAccountsHandler),  # 账目汇总
    url(r"/config/order/generateExcel", GetConfigOrderGeneralExcelHandler),  # 订单列表导出excel
    url(r"/config/order/downloadExcel", GetConfigOrderDownLoadExcelHandler),  # 订单列表下载文件
]
