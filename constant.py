#!/usr/bin/pyhton
# -*- coding: utf-8 -*-
# @Author: xiaoli
# @Time: 2019/5/25
PAGE_SHOW_COUNT = 15  # 每页显示多少条数据
IMG_CODE_EXPIRES_SECONDS = 300  # 图片验证码有效期, 单位秒
SESSION_EXPIRES_SECONDS = 86400  # session数据有效期, 单位秒
REMEMBER_SESSION_EXPIRES_SECONDS = 604800  # session数据有效期, 单位秒
SECRET = "QWHFOGVHSW)*&%#JKDLHF&#$J9JFUEDHJ"  # jwt生成token值所需要的盐


# redis中的键名
Constants = {
    "REDIS_PERMISSION_LIST": "PermissionList:",  # 菜单管理
    "REDIS_CONFIG_MENU_USERMENULIST": "ConfigMenuUserMenuList",  # 获取到首页菜单
    "REDIS_CONFIG_SYS_USER_LIST": "ConfigSysUserList:",  # 用户管理所有信息展示
    "REDIS_CONFIG_SYS_ROLE_LIST": "ConfigSysRoleList:",  # 角色管理所有信息展示
    "REDIS_CONFIG_SYS_LOG_LIST": "ConfigSyslogList:",  # 日志管理所有信息展示
    "REDIS_CONFIG_BLACK_WHITE_BLACK_LIST": "ConfigBlackWhiteBlackList:",  # 用户黑名单所有信息展示
    "REDIS_CONFIG_BLACK_WHITE_WHITE_LIST": "ConfigBlackWhiteWhiteList:",  # 系统白名单所有信息展示
    "REDIS_CONFIG_LOOK_UP_GROUP_LIST": "ConfigLookUpGroupList:",  # LOOKUP管理所有信息展示
    "REDIS_CONFIG_DICTIONARY_LIST": "ConfigDictionaryList:",  # 数据字典所有信息展示
    "REDIS_CONFIG_PAY_INFO_ALL": "ConfigPayInfoAll:",  # 支付通道所有信息展示
    "REDIS_CONFIG_PAY_API_LIST": "ConfigPayApiList:",  # 支付平台所有信息展示
    "REDIS_LOOK_ITEM_GROUP_CODE_PAGE": "LookItemGroupCodePage:",  # 支付类型所有信息展示
    "REDIS_CONFIG_PAY_CODE_VIEW": "ConfigPayCodeView:",  # 支付二维码所有信息展示
    "REDIS_CONFIG_GROUP_GROUP_LIST": "ConfigGroupGroupList:",  # 会员分级所有信息展示
    "REDIS_CONFIG_CUSTOMER_CUSTOMER_LIST": "ConfigCustomerCustomerList",  # 会员列表所有信息展示
    "REDIS_CONFIG_CACHE_CODE": "ConfigCacheCode",  # 验证码
}