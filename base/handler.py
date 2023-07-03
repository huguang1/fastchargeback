#!/usr/bin/pyhton
# -*- coding: utf-8 -*-
# @Author: xiaoli
# @Time: 2019/5/25
from tornado.web import RequestHandler
from utils.restful import unauth, forbidden


class BaseHandler(RequestHandler):
    @property
    def redis_conn(self):
        return self.application.redis

    # 重置请求头，或者说是响应头
    def set_default_headers(self) -> None:
        self.set_header('Content-type', 'application/json; charset=UTF-8')

    def get_current_user(self):
        """ 判断用户是否登录 """
        session_id = self.get_secure_cookie('session_id')
        if session_id:
            session_id = str(session_id, encoding='utf-8')
        a = self.redis_conn.get('sess_%s' % session_id)
        return a

    def on_finish(self):
        """ 请求结束调用  """
        # self.session.flush()
        pass


class GetUserHandler(BaseHandler):
    async def prepare(self):
        if not self.current_user:
            content = unauth(message='这个用户没有登陆')
            return await self.finish(content)


class CheckTokenHandler(BaseHandler):
    # CSRF验证
    async def prepare(self):
        if not self.current_user:
            content = unauth(message='这个用户没有登陆')
            return await self.finish(content)
        cookie_token = self.get_cookie('token')
        header_token = self.request.headers["X-Csrf-Token"]
        if cookie_token != header_token:
            content = forbidden(message='这个是错误的!')
            return await self.finish(content)
