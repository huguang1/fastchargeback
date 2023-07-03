#!/usr/bin/pyhton
# -*- coding: utf-8 -*-
# @Author: xiaoli
# @Time: 2019/5/25
import datetime
import random


def generate_order_id():
    return datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(0, 9))
