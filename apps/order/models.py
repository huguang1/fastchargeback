#!/usr/bin/pyhton
# -*- coding: utf-8 -*-
# @Author: xiaoli
# @Time: 2019/5/25
from peewee import *
from base.models import BaseModel


# 订单
class TOrder(BaseModel):
    user_account = CharField(max_length=20, null=True)  # 用户名
    order_id = CharField(unique=True, max_length=255, null=True)  # 订单编码
    order_amount = DecimalField(max_digits=10, decimal_places=2, null=True)  # 订单金额
    #  支付状态 INIT(0, "全部状态"), PAYING(10, "支付处理中"),PAY_FILED(20, "支付失败"), PAY_SUCCESS(30,"支付成功");
    order_state = IntegerField(null=True)  # 订单状态
    order_desc = CharField(max_length=255, null=True)
    order_time = DateTimeField(null=True)
    user_ip = CharField(max_length=50, null=True)
    payment_code = CharField(max_length=255, null=True)  # 订单来源
    pay_code = CharField(max_length=100, null=True)
    pay_order = CharField(max_length=255, null=True)
    item_code = CharField(max_length=255, null=True)  # 支付方式
    #  ALL(0, "全部状态"), OPE_TO_DO(10, "待处理"), OPE_LOCKED(20, "已锁定"), OPE_TO_CONFIRM(30, "待确认"),
    #  OPE_CONFIRM(40, "已确定" ),OPE_CANCEL(50, "已取消")
    state = IntegerField(null=True)
    rate = DecimalField(max_digits=10, decimal_places=2, null=True)
    # 手续费
    rate_amount = DecimalField(max_digits=10, decimal_places=2, null=True)
    lock_id = CharField(max_length=20, null=True)
    external_id = IntegerField(null=True)
    update_time = DateTimeField(null=True)
    update_user = CharField(max_length=30, null=True)

    class Meta:
        db_table = 't_order'


# 每日订单统计
class TOrderDaliySum(BaseModel):
    order_date = DateField(primary_key=True)
    number = IntegerField(null=True)
    amount = DecimalField(max_digits=10, decimal_places=2, null=True)
    amount_rate = DecimalField(max_digits=10, decimal_places=2, null=True)
    order_state = DecimalField(max_digits=10, decimal_places=2, null=True)
    amount_success = DecimalField(max_digits=20, decimal_places=2, null=True)
    amount_fail = DecimalField(max_digits=20, decimal_places=2, null=True)
    number_success = IntegerField(null=True)
    number_fail = IntegerField(null=True)
    on_pay_order_id = CharField(max_length=255, null=True)

    class Meta:
        db_table = 't_order_daliy_sum'


# 历史订单列表
class TOrderHis(BaseModel):
    user_account = CharField(max_length=20, null=True)  # 用户名
    order_id = CharField(unique=True, max_length=255, null=True)  # 订单编码
    order_amount = DecimalField(max_digits=10, decimal_places=2, null=True)  # 订单金额
    order_state = IntegerField(null=True)  # 订单状态
    order_desc = CharField(max_length=255, null=True)
    order_time = DateTimeField()
    user_ip = CharField(max_length=50, null=True)
    payment_code = CharField(max_length=255, null=True)  # 订单来源
    pay_code = CharField(max_length=100, null=True)
    pay_order = CharField(max_length=255, null=True)
    item_code = CharField(max_length=255, null=True)  # 支付方式
    state = IntegerField(null=True)
    rate = DecimalField(max_digits=10, decimal_places=2, null=True)
    # 手续费
    rate_amount = DecimalField(max_digits=10, decimal_places=2, null=True)
    lock_id = CharField(max_length=20, null=True)
    update_time = DateTimeField()
    update_user = CharField(max_length=30, null=True)
    batch_no = IntegerField()

    class Meta:
        db_table = 't_order_his'
