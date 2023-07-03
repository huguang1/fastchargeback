#!/usr/bin/pyhton
# -*- coding: utf-8 -*-
# @Author: xiaoli
# @Time: 2019/5/25
from apps.cfg import urls as cfg_urls
from apps.order import urls as order_urls
from apps.pay import urls as pay_urls
from apps.system import urls as system_urls

urlpattern = []

urlpattern += cfg_urls.urlpattern
urlpattern += order_urls.urlpattern
urlpattern += pay_urls.urlpattern
urlpattern += system_urls.urlpattern
