from nonebot import on_notice, NoticeSession
import config as config
from .txt_tools import add_at

# 将函数注册为群成员增加通知处理器
@on_notice('group_increase')
async def _(session: NoticeSession):
    # 发送欢迎消息
    if str(session.ctx.get('group_id')) in config.while_list:
        reply = '欢迎新朋友～，我是哈工深问答机器人小哈，欢迎向我提问哦！\n提问示例：小哈 怎么填志愿才能上哈深？'
        reply = add_at(reply, session.ctx.get('user_id'))
        await session.send(reply)