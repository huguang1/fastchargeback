#!/usr/bin/pyhton
# -*- coding: utf-8 -*-
# @Author: xiaoli
# @Time: 2019/5/25
from peewee import *
from base.models import BaseModel, DBModel


# 日志管理
class SysLog(BaseModel):
    log_ip = CharField(max_length=50, null=True)  # IP
    business = CharField(max_length=50, null=True)  # 日志内容
    log_user = CharField(max_length=50, null=True)  # 操作人
    model = CharField(max_length=50, null=True)   # 模块
    log_params = CharField(max_length=2000, null=True)  # 参数

    class Meta:
        db_table = 'sys_log'


# 菜单管理
class SysPermission(BaseModel):
    # 权限路径
    url = CharField(max_length=100)  # 菜单地址
    # 描述
    description = CharField(max_length=100, null=True)  # 菜单名称
    # permission_id
    pid = IntegerField(null=True)
    # 菜单图标
    icon = CharField(max_length=255, null=True)  # 菜单图标
    # 菜单排序
    model_order = IntegerField(null=True)  # 菜单排序
    # 菜单分级(1:1级菜单;2:2级菜单;3:3级菜单)
    model_level = IntegerField(null=True)
    # 父级菜单id
    parent_id = IntegerField(null=True)
    # 有子菜单(1:有;0:无)
    has_child = IntegerField(null=True)
    # 路径类型（1:菜单;2:button;3:路径）
    permission_type = IntegerField(null=True)
    # 创建人
    create_user = CharField(max_length=100, null=True)
    # 更新时间
    update_time = DateTimeField()
    # 更新人
    update_user = CharField(max_length=100, null=True)

    class Meta:
        db_table = 'sys_permission'


# 角色管理
class SysRole(DBModel):
    role_name = CharField(max_length=20, null=True)  # 角色名称
    role_desc = CharField(max_length=20, null=True)  # 角色描述

    class Meta:
        db_table = 'sys_role'


# 外键表
class SysRolePermission(DBModel):
    role_id = IntegerField()
    pers_id = IntegerField(null=True)

    class Meta:
        db_table = 'sys_role_permission'


# 用户管理
class SysUser(BaseModel):
    user_name = CharField(unique=True, max_length=100, null=True)  # 用户名
    nick_name = CharField(max_length=100, null=True)  # 昵称
    password = CharField(max_length=100, null=True)  # 密码
    last_login_time = DateTimeField(null=True)  # 上次登陆时间
    login_ip = CharField(max_length=255, null=True)  # 登陆IP
    level = IntegerField(null=True)
    state = IntegerField(null=True)
    update_time = DateTimeField()

    class Meta:
        db_table = 'sys_user'


# 外键表
class SysUserRole(DBModel):
    user_id = IntegerField(null=True)
    role_id = IntegerField(null=True)

    class Meta:
        db_table = 'sys_user_role'


# 系统白名单
class WhiteBlackList(BaseModel):
    ip = CharField(max_length=255, null=True)  # IP地址
    user_name = CharField(max_length=255, null=True)  # 会员名称
    role_type = IntegerField(null=True)
    remarks = CharField(max_length=255, null=True)  # 备注
    create_user = CharField(max_length=255, null=True)
    update_time = DateTimeField(null=True)
    update_user = CharField(max_length=255, null=True)

    class Meta:
        db_table = 'white_black_list'


# LOOKUP管理
class TLookupGroup(BaseModel):
    group_code = CharField(unique=True, max_length=20, null=True)  # 编码
    group_name = CharField(unique=True, max_length=50, null=True)  # 名称
    state = IntegerField(null=True)  # 状态
    parent_group_code = CharField(max_length=50, null=True)  # 父ID
    create_user = CharField(max_length=20, null=True)
    update_user = CharField(max_length=20, null=True)
    udpate_time = DateTimeField()

    class Meta:
        db_table = 't_lookup_group'


# 数据字典
class TDictionary(DBModel):
    dic_key = CharField(max_length=1, null=True)  # 字典key
    dic_value = CharField(max_length=2, null=True)  # 字典值
    description = CharField(max_length=2, null=True)  # 字典描述

    class Meta:
        db_table = 't_dictionary'
