#!/usr/bin/pyhton
# -*- coding: utf-8 -*-
# @Author: xiaoli
# @Time: 2019/5/25
from datetime import datetime
from config import mysql_db
from peewee import *


# 这里面的Model是负担其增删改查任务的类
# DateTimeField字段类，是建立具体字段的类，负责排序上的工作
class BaseModel(Model):
    create_time = DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        database = mysql_db


class DBModel(Model):

    class Meta:
        database = mysql_db