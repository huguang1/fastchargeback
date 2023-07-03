#!/usr/bin/pyhton
# -*- coding: utf-8 -*-
# @Author: xiaoli
# @Time: 2019/5/25
from tornado.web import url
from .handler import GetConfigPayInfoAllHandler, GetConfigPayApiListHandler, GetConfigPayCodeViewHandler, \
    GetLookUpItemByGroupCodePageHandler, GetConfigPayCodeGetListHandler, UpdateConfigPayCodeStatusHandler, \
    CreateConfigPayCodeFileUploadHandler, DeleteConfigPayCodeHandler, CreateConfigLookUpItemSaveHandler, \
    DeleteConfigLookUpItemHandler, GetConfigLookUpItemInfoHandler, CreateConfigPayApiSaveHandler, \
    DeleteConfigPayApiByIdHandler, GetConfigPayApiInfoHandler, CreateConfigPayInfoSaveHandler, DeleteConfigPayInfoHandler, \
    GetConfigPayInfoInfoHandler, GetLookUpItemByGroupCodeHandler

urlpattern = [
    url(r"/config/payinfo/all", GetConfigPayInfoAllHandler),  # 支付通道所有信息展示
    url(r"/config/payapi/list", GetConfigPayApiListHandler),  # 支付平台所有信息展示
    url(r"/config/lookupitem/getLookupItemByGroupCodePage", GetLookUpItemByGroupCodePageHandler),  # 支付类型所有信息展示
    url(r"/config/lookupitem/getLookupItemByGroupCode", GetLookUpItemByGroupCodeHandler),  # 获取某个支付类型信息
    url(r"/config/payCode/payCodeView", GetConfigPayCodeViewHandler),  # 支付二维码所有信息展示
    url(r"/config/payCode/getList", GetConfigPayCodeGetListHandler),  # 支持二维码的支付通道
    url(r"/config/payCode/filesUpload", CreateConfigPayCodeFileUploadHandler),  # 添加二维码
    url(r"/config/payCode/deleteCode", DeleteConfigPayCodeHandler),  # 删除二维码
    url(r"/config/payCode/updateCodeState", UpdateConfigPayCodeStatusHandler),  # 更改二维码
    url(r"/config/lookupitem/save", CreateConfigLookUpItemSaveHandler),  # 增加支付类型，修改支付类型
    url(r"/config/lookupitem/deleteById", DeleteConfigLookUpItemHandler),  # 删除支付类型
    url(r"/config/lookupitem/info", GetConfigLookUpItemInfoHandler),  # 获取到某个支付类型的所有信息
    url(r"/config/payapi/save", CreateConfigPayApiSaveHandler),  # 增加支付平台
    url(r"/config/payapi/deleteById", DeleteConfigPayApiByIdHandler),  # 删除支付平台
    url(r"/config/payapi/info", GetConfigPayApiInfoHandler),  # 获取某个支付平台的详细信息
    url(r"/config/payinfo/save", CreateConfigPayInfoSaveHandler),  # 添加支付通道
    url(r"/config/payinfo/deleteById", DeleteConfigPayInfoHandler),  # 删除支付通道
    url(r"/config/payinfo/info", GetConfigPayInfoInfoHandler),  # 获取某个支付通道的信息
]
