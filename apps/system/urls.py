#!/usr/bin/pyhton
# -*- coding: utf-8 -*-
# @Author: xiaoli
# @Time: 2019/5/25
from tornado.web import url
from .handler import GetUserNameHandler, GetSysUserListHandler, GetSysRoleListHandler, GetSysLogListHandler, \
    GetConfigBlackWhiteBlackListHandler, GetConfigBlackWhiteWhiteListHandler, GetConfigLookUpGroupListHandler, \
    GetConfigDictionaryListHandler, GetLoginHandler, GetConfigCacheHandler, GetConfigGetLoginToken, LogoutHandler, \
    CreateConfigDictionarySaveHandler,MenuUuserMenuListHandler,PermissionListHandler,DeleteConfigDictionaryDelHandler,\
    UpdateConfigDictionaryUpdateHandler, CreateConfigLookupGroupSaveHandler, DeleteConfigLookupGroupDeleteByIdHandler, \
    GetConfigLookUpGroupInfoHandler, CreateConfigBlackWhiteAddWhiteHandler, DeleteConfigBlackWhiteDeleteHandler, \
    DeleteConfigBlackWhiteBatchDeleteHandler,CreateConfigBlackWhiteAddBlackHandler,DeleteConfigSysLogBatchDeleteHandler,\
    DeleteConfigSysLogClearLogHandler, CreateConfigSysPermissionHandler, DeleteConfigSysPermissionHandler, \
    UpdateConfigSysPermissionHandler, CreateConfigSysRoleHandler, DeleteConfigSysRoleHandler, \
    GetConfigSysRoleQueryPermissionHandler, UpdateConfigSysRoleHandler, CreateConfigSysUserHandler, \
    DeleteConfigSysUserHandler, UpdateConfigSysUserHandler

urlpattern = [
    url(r"/check/login", GetLoginHandler),  # 登陆校验返回token值
    url(r"/config/cache", GetConfigCacheHandler),  # 验证码
    url(r"/config/getlogin/token", GetConfigGetLoginToken),  # 获取验证登陆页面的token值
    url(r"/config/init/getUserName", GetUserNameHandler),  # 获取登陆管理员
    url(r"/logout", LogoutHandler),  # 用户登出页面
    url(r"/config/menu/userMenuList", MenuUuserMenuListHandler),  # 获取到首页菜单
    url(r"/config/sys/permission/list", PermissionListHandler),  # 菜单管理所有信息展示
    url(r"/config/sys/user/list", GetSysUserListHandler),  # 用户管理所有信息展示
    url(r"/config/sys/role/list", GetSysRoleListHandler),  # 角色管理所有信息展示
    url(r"/config/sys/log/list", GetSysLogListHandler),  # 日志管理所有信息展示
    url(r"/config/blackWhite/blackList", GetConfigBlackWhiteBlackListHandler),  # 用户黑名单所有信息展示
    url(r"/config/blackWhite/whiteList", GetConfigBlackWhiteWhiteListHandler),  # 系统白名单所有信息展示
    url(r"/config/lookupgroup/list", GetConfigLookUpGroupListHandler),  # LOOKUP管理所有信息展示
    url(r"/config/dictionary/list", GetConfigDictionaryListHandler),  # 数据字典所有信息展示
    url(r"/config/dictionary/save", CreateConfigDictionarySaveHandler),  # 添加数据字典
    url(r"/config/dictionary/del/(.+)", DeleteConfigDictionaryDelHandler),  # 删除字典数据
    url(r"/config/dictionary/update", UpdateConfigDictionaryUpdateHandler),  # 修改字典数据
    url(r"/config/lookupgroup/save", CreateConfigLookupGroupSaveHandler),  # 添加lookup数据
    url(r"/config/lookupgroup/deleteById", DeleteConfigLookupGroupDeleteByIdHandler),  # 删除lookup数据
    url(r"/config/lookupgroup/info", GetConfigLookUpGroupInfoHandler),  # 修改lookup数据,先查询这个lookup的信息
    url(r"/config/blackWhite/addWhite", CreateConfigBlackWhiteAddWhiteHandler),  # 添加系统白名单数据
    url(r"/config/blackWhite/delete", DeleteConfigBlackWhiteDeleteHandler),  # 删除系统黑白名单数据
    url(r"/config/blackWhite/batchDelete", DeleteConfigBlackWhiteBatchDeleteHandler),  # 删除多个系统黑白名单
    url(r"/config/blackWhite/addBlack", CreateConfigBlackWhiteAddBlackHandler),  # 添加用户黑名单
    url(r"/config/sys/log/batchDelete", DeleteConfigSysLogBatchDeleteHandler),  # 删除多个日志管理记录
    url(r"/config/sys/log/clearlog", DeleteConfigSysLogClearLogHandler),  # 清空日志管理记录
    url(r"/config/sys/permission/save", CreateConfigSysPermissionHandler),  # 添加菜单管理
    url(r"/config/sys/permission/delete", DeleteConfigSysPermissionHandler),  # 删除菜单管理
    url(r"/config/sys/permission/update", UpdateConfigSysPermissionHandler),  # 修改菜单管理
    url(r"/config/sys/role/save", CreateConfigSysRoleHandler),  # 添加角色管理
    url(r"/config/sys/role/delete", DeleteConfigSysRoleHandler),  # 删除角色管理
    url(r"/config/sys/role/queryPermisson", GetConfigSysRoleQueryPermissionHandler),  # 修改角色管理之前,需要查看角色由什么权限
    url(r"/config/sys/role/update", UpdateConfigSysRoleHandler),  # 修改角色管理
    url(r"/config/sys/user/save", CreateConfigSysUserHandler),  # 添加用户管理
    url(r"/config/sys/user/delete", DeleteConfigSysUserHandler),  # 删除用户管理
    url(r"/config/sys/user/updateUser", UpdateConfigSysUserHandler),  # 修改用户管理
]
