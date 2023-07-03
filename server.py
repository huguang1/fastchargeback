#!/usr/bin/pyhton
# -*- coding: utf-8 -*-
# @Author: xiaoli
# @Time: 2019/5/25
from tornado import web, ioloop
import config
import redis
from base.urls import urlpattern
from peewee_async import Manager
from tornado.options import define, options
from config import mysql_db as db
define("port", default=8001, help="run on th given port", type=int)


class Application(web.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        rdp = redis.ConnectionPool(**config.redis_option)  # 创建redis进程池
        self.redis = redis.StrictRedis(connection_pool=rdp)  # 创建redis连接


if __name__ == '__main__':
    options.log_file_prefix = config.log_path  # 将日志保存在文件中
    options.logging = config.log_level  # 设置日志等级
    options.parse_command_line()  # 转换命令行参数

    app = Application(
        urlpattern,
        **config.setting,
    )

    app.listen(options.port, xheaders=True)  # 服务器监听端口
    objects = Manager(db)
    db.set_allow_sync(False)
    app.objects = objects
    ioloop.IOLoop.current().start()
