#!/usr/bin/pyhton
# -*- coding: utf-8 -*-
# @Author: xiaoli
# @Time: 2019/5/25
from peewee import *
from base.models import BaseModel


# 会员列表
class TCustomerUser(BaseModel):
    user_account = CharField(unique=True, max_length=20, null=True)  # 会员账号
    level = IntegerField(null=True)
    amounts = DecimalField(max_digits=13, decimal_places=2, null=True)
    group_id = IntegerField(null=True)  # 级别编号
    remark = CharField(max_length=255, null=True)
    update_time = DateTimeField()

    class Meta:
        db_table = 't_customer_user'


# 会员分级
class TGroup(BaseModel):
    name = CharField(max_length=50, null=True)  # 分级名称
    state = IntegerField(null=True)
    str_values = CharField(max_length=1000, null=True)  # 支持的付款方式
    remark = CharField(max_length=100,  null=True)
    create_user = CharField(max_length=20, null=True)
    update_user = CharField(max_length=20, null=True)
    update_time = DateTimeField()

    class Meta:
        managed = False
        db_table = 't_group'


# bbin订单类
class TGamePlatFormOrder(BaseModel):
    number = CharField(max_length=255, null=True)
    order_id = CharField(max_length=255, null=True)
    amount = DecimalField(max_digits=12, decimal_places=2, null=True)
    created_at = CharField(max_length=255, null=True)
    username = CharField(max_length=255, null=True)
    notify_url = CharField(max_length=255, null=True)
    method_id = CharField(max_length=255, null=True)
    bank_id = CharField(max_length=255, null=True)
    sign = CharField(max_length=255, null=True)
    status = IntegerField(null=True)
    notify_time = DateTimeField()

    class Meta:
        db_table = 't_game_platform_order'
