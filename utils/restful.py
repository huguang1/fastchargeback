#!/usr/bin/pyhton
# -*- coding: utf-8 -*-
# @Author: xiaoli
# @Time: 2019/5/25
import json
from utils.json import DecimalEncoder


class httpCode(object):
    # 成功返回数据
    data = 0

    # 成功
    ok = 200

    # 参数错误
    paramserror = 400

    # 未授权
    unauth = 401

    # 禁止
    forbidden = 403

    # 方法错误
    methoderror = 405

    # 服务器内部错误
    servererror = 500


def result(code=httpCode.ok, message='', data=None, kwargs=None):
    """"
    数据格式(json)：{'code': code, 'message': message, 'data': data}
    code：状态码
    message：错误信息
    data：json格式数据
    """

    json_dict = {"code": code, "message": message, "data": data}

    if kwargs and isinstance(kwargs, dict) and kwargs.keys():
        json_dict.update(kwargs)

    return json.dumps(json_dict, cls=DecimalEncoder)


def data(message='', data=None, kwargs=None):
    return result(httpCode.data, message, data, kwargs)


def ok():
    return result()


def params_error(message='', data=None):
    """
    参数错误
    :param message:
    :param data:
    :return:
    """
    return result(httpCode.paramserror, message, data)


def unauth(message='', data=None):
    """
    未授权
    :param message:
    :param data:
    :return:
    """
    return result(httpCode.unauth, message, data)


def forbidden(message='', data=None):
    """
    禁止
    :param message:
    :param data:
    :return:
    """
    return result(httpCode.forbidden, message, data)


def method_error(message='', data=None):
    """
    方法错误
    :param message:
    :param data:
    :return:
    """
    return result(httpCode.methoderror, message, data)


def server_error(message='', data=None):
    return result(httpCode.servererror, message, data)


