#!/usr/bin/pyhton
# -*- coding: utf-8 -*-
# @Author: xiaoli
# @Time: 2019/5/25
import os
import peewee_async
# 基本的目录路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Application 配置参数
setting = {
    "cookie_secret": "qADCZPWsT5qVcL3O6XFvEcuB2tsD801TiymNS48MVFk=",
    "debug": True,
    "static_path": os.path.join(BASE_DIR, "static"),
}

# mysql
mysql_db = peewee_async.PooledMySQLDatabase(
    "carea_pay",
    host="localhost",
    port=3306,
    user="root",
    password="mysql",
    min_connections=1,
    max_connections=10,
)

# redis
redis_option = dict(
    host="127.0.0.1",
    port=6379,
    db=6,
    decode_responses=True
)

# logg
# tail -f log 实时查看日志
log_path = os.path.join(BASE_DIR, "logs/fast_charge_back.log")
log_level = "debug"

# Password key
passwd_hash_key = "WIEyGvZ4T+i2Gi/8PGs1gz6ocDUtlU5AphBGUIaRc8Y="
