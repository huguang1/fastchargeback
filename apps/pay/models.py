#!/usr/bin/pyhton
# -*- coding: utf-8 -*-
# @Author: xiaoli
# @Time: 2019/5/25
from peewee import *
from base.models import BaseModel, DBModel


# 支付平台
class TPayApi(BaseModel):
    payment_code = CharField(unique=True, max_length=20, null=True)  # 平台编码
    payment_name = CharField(max_length=50, null=True)  # 平台名称
    state = IntegerField(null=True)  # 状态
    memberid = CharField(max_length=50, null=True)  # 商户ID
    api_key = CharField(max_length=2000, null=True)  # apikey
    http_url = CharField(max_length=100, null=True)  # 请求地址
    http_type = CharField(max_length=10, null=True)  # 请求方式
    notify_url = CharField(max_length=100, null=True)
    notify_type = CharField(max_length=16, null=True)  # 回调类型
    callback_url = CharField(max_length=100, null=True)
    query_url = CharField(max_length=100, null=True)
    sign_type = CharField(max_length=50, null=True)
    sign_format = CharField(max_length=2000, null=True)
    param_format = CharField(max_length=2000, null=True)
    verify_format = CharField(max_length=2000, null=True)
    remark = CharField(max_length=200, null=True)  # 备注
    attribute_1 = CharField(max_length=400, null=True)
    attribute_2 = CharField(max_length=400, null=True)
    attribute_3 = CharField(max_length=1000, null=True)
    attribute_4 = CharField(max_length=2000, null=True)
    attribute_5 = CharField(max_length=2000, null=True)
    create_user = CharField(max_length=20, null=True)
    update_user = CharField(max_length=20, null=True)
    udpate_time = DateTimeField()

    class Meta:
        db_table = 't_pay_api'


# 支付二维码
class TPayCode(DBModel):
    code = TextField()  # 付款二维码
    comment = CharField(max_length=50, null=True)  # 备注
    pay_code = CharField(max_length=50, null=True)  # 支付类型
    status = IntegerField()  # 状态

    class Meta:
        db_table = 't_pay_code'


# 支付通道
class TPayInfo(BaseModel):
    payment_code = CharField(max_length=20, null=True)
    payment_name = CharField(max_length=50, null=True)  # 平台名称
    pay_code = CharField(max_length=255, null=True)  # 支付编码
    item_name = CharField(max_length=50, null=True)  # 支付类型名称
    item_code = CharField(max_length=50, null=True)
    pay_model = IntegerField()  # 支付设备
    icon = CharField(max_length=255, null=True)  # 图标名称
    rate = DecimalField(max_digits=10, decimal_places=2, null=True)  # 比例/费用
    rate_type = IntegerField(null=True)  # 佣金类型
    state = IntegerField(null=True)  # 状态
    min_switch = CharField(max_length=4, null=True)  # 最小金额开关
    min_amount = DecimalField(max_digits=11, decimal_places=2, null=True)  # 最小金额
    max_amount = DecimalField(max_digits=11, decimal_places=2, null=True)  # 最大金额
    max_switch = CharField(max_length=4, null=True)  # 最大金额开关
    point_switch = CharField(max_length=4, null=True)  # 小数开关
    bank_code = CharField(max_length=32, null=True)
    create_user = CharField(max_length=20, null=True)
    update_user = CharField(max_length=20, null=True)
    udpate_time = DateTimeField()

    class Meta:
        db_table = 't_pay_info'


# 支付类型
class TLookupItem(BaseModel):
    item_code = CharField(max_length=20, null=True)  # 类型编码
    item_name = CharField(max_length=50, null=True)  # 类型名称
    sort = IntegerField(null=True)  # 排序
    state = IntegerField(null=True)  # 状态
    group_code = CharField(max_length=20, null=True)
    parent_item_code = CharField(max_length=20, null=True)
    attribute_1 = CharField(max_length=100, null=True)
    attribute_2 = CharField(max_length=100, null=True)  # 最小金额
    attribute_3 = CharField(max_length=100, null=True)  # 最大金额
    attribute_4 = CharField(max_length=100, null=True)  # 图标
    attribute_5 = CharField(max_length=100, null=True)
    create_user = CharField(max_length=20, null=True)
    update_user = CharField(max_length=20, null=True)
    udpate_time = DateTimeField()

    class Meta:
        db_table = 't_lookup_item'
