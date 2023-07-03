#!/usr/bin/pyhton
# -*- coding: utf-8 -*-
# @Author: xiaoli
# @Time: 2019/5/25
from tornado.web import url
from apps.cfg.handler import GetConfigGroupListHandler, GetConfigCustomerListHandler, CreateConfigGroupSaveHandler, \
    DeleteConfigGroupDelHandler, GetConfigGroupFindHandler, UpdateConfigGroupUpdHandler, GetConfigGroupBoxHandler, \
    CreateConfigCustomerSaveHandler, DeleteConfigCustomerDelHandler, DeleteConfigCustomerBatchDelHandler, \
    GetConfigCustomerDownMemberTempHandler, UpConfigCustomerUpdHandler

urlpattern = [
    url(r"/config/group/groupList", GetConfigGroupListHandler),  # 会员分级所有信息展示
    url(r"/config/group/save", CreateConfigGroupSaveHandler),  # 添加会员分级
    url(r"/config/group/del", DeleteConfigGroupDelHandler),  # 删除会员分级
    url(r"/config/group/find", GetConfigGroupFindHandler),  # 查询某个会员分级信息
    url(r"/config/group/upd", UpdateConfigGroupUpdHandler),  # 修改会员分级信息
    url(r"/config/customer/customerList", GetConfigCustomerListHandler),  # 会员列表所有信息展示
    url(r"/config/group/box", GetConfigGroupBoxHandler),  # 获取会员分级的种类
    url(r"/config/customer/save", CreateConfigCustomerSaveHandler),  # 添加会员账号
    url(r"/config/customer/del", DeleteConfigCustomerDelHandler),  # 删除会员
    url(r"/config/customer/batchdel", DeleteConfigCustomerBatchDelHandler),  # 批量删除会员
    url(r"/config/customer/downMemberTemp", GetConfigCustomerDownMemberTempHandler),  # 会员列表下载模板
    url(r"/config/customer/upd", UpConfigCustomerUpdHandler),  # 会员列表上传文件
]
