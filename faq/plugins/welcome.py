from nonebot import on_notice, NoticeSession

import config as config
from .txt_tools import add_at


# 将函数注册为群成员增加通知处理器
# @on_notice('group_increase')
async def _(session: NoticeSession):
    # 发送欢迎消息
    if str(session.ctx.get('group_id')) in config.welcome_list:
        reply = '为了能更好的给您提供招生咨询服务，请您先规范群名片格式：高考省份简称+高考年份+F(父)/M(母)+网名+B/G考生男孩女孩，谢谢您的配合。\n改完群名片，您可以先看看群文件，群相册，有问题的可以提问，群里有招生老师、哈深学子、家长和问答机器人为您答疑。\n我是小哈，在问题开头加上“小哈”即可向我提问哦~'
        reply = add_at(reply, session.ctx.get('user_id'))
        await session.send(reply)
