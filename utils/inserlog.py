from apps.system.models import SysLog
import logging


async def log(self, action):
    ip = self.request.remote_ip
    user = self.current_user
    if await self.application.objects.create(SysLog, log_ip=ip, business=action, log_user=user, model='用户', log_params=user):
        logging.error('%s失败' % action)
    else:
        logging.info('%s成功' % action)
