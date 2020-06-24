# encoding:utf-8
import json
import os
import bot.config as config
import aiohttp
from aiocqhttp.message import escape
from typing import Optional
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot.helpers import context_id, render_expression
from nn.RequestHandler import RequestHandler
from ..txt_tools import raw_to_answer, add_at

rh_sub = RequestHandler(1)
Q2A_dict = {}
log_list = []
current_path = os.path.dirname(__file__)
path = current_path + '/answers.txt'

with open(path, 'r', encoding='UTF-8') as file:
    lines = file.readlines()
    for line in lines:
        tmp_list = line.split('\t')
        Q2A_dict[tmp_list[0]] = tmp_list[1]


@on_command('faq_local')
async def faq_local(session: CommandSession):
    question = session.state.get('message')
    reply, confidence = await test_local(question)
    if confidence < config.CONFIDENCE:
        # tuling_reply = await call_tuling_api(session, question)  # 闲聊调用图灵机器人
        # if "图灵" in tuling_reply or "限制" in tuling_reply or "http" in tuling_reply:
        #     reply = render_expression(EXPR_DONT_UNDERSTAND)
        # elif tuling_reply:
        #     reply = tuling_reply
        # else:
        reply = render_expression(config.EXPR_DONT_UNDERSTAND)
    reply = add_at(reply, session.ctx.get('user_id'))
    await session.send(reply)


@on_natural_language
async def _(session: NLPSession):
    if str(session.ctx.get('sub_type')) == 'friend' or str(session.ctx.get('group_id')) in config.while_list:
        return IntentCommand(80.0, 'faq_local', args={'message': session.msg_text})


async def test_local(message):
    ans, confidence = rh_sub.getResult(message)
    log = message + '\t__label__' + ans + '\t' + str(round(confidence, 2)) + '\n'  # 记录问题和预测标签、置信度
    global log_list
    log_list.append(log)  # 保存日志到 log_list
    if len(log_list) >= config.LOG_SAVE_LEN:
        log_save()  # 日志长度大等于 LOG_SAVE_LEN 时，写入文件
    ans = Q2A_dict[ans]
    ans = raw_to_answer(ans)
    ans = '测试中：\n' + ans
    return ans, confidence


async def call_tuling_api(session: CommandSession, text: str) -> Optional[str]:
    # 调用图灵机器人的 API 获取回复

    if not text:
        return None

    url = 'http://openapi.tuling123.com/openapi/api/v2'

    # 构造请求数据
    payload = {
        'reqType': 0,
        'perception': {
            'inputText': {
                'text': text
            }
        },
        'userInfo': {
            'apiKey': session.bot.config.TULING_API_KEY,
            'userId': context_id(session.ctx, use_hash=True)
        }
    }

    group_unique_id = context_id(session.ctx, mode='group', use_hash=True)
    if group_unique_id:
        payload['userInfo']['groupId'] = group_unique_id

    try:
        # 使用 aiohttp 库发送最终的请求
        async with aiohttp.ClientSession() as sess:
            async with sess.post(url, json=payload) as response:
                if response.status != 200:
                    # 如果 HTTP 响应状态码不是 200，说明调用失败
                    return None

                resp_payload = json.loads(await response.text())
                if resp_payload['results']:
                    for result in resp_payload['results']:
                        if result['resultType'] == 'text':
                            # 返回文本类型的回复
                            return result['values']['text']
    except (aiohttp.ClientError, json.JSONDecodeError, KeyError):
        # 抛出上面任何异常，说明调用失败
        return None


def log_save():
    global log_list
    f = open('log.txt', 'a', encoding='UTF-8')
    f.writelines(log_list)
    log_list = []
    f.close()

# async def faq(session: CommandSession):
#     question = session.state.get('message')
#     at = "[CQ:at,qq="
#     at += str(session.ctx.get('user_id'))
#     at += "]\n"
#     reply = await test(question)
#     if reply:
#         if reply == {}:
#             reply = {'1': ['', '']}
#         confidence = float(list(reply.keys())[0])
#         answer = list(reply.values())[0][1]
#         if confidence < config.CONFIDENCE:
#             rule = "%img\d%\(\d\)(\s\d+)+"
#             answer = re.sub(rule, cqp_replace, answer)
#             answer = answer.replace("\\n", "\n")
#             at += answer
#         else:
#             reply = await call_tuling_api(session, question)
#             if "图灵" in reply or "限制" in reply:
#                 random = render_expression(EXPR_DONT_UNDERSTAND)
#                 at += random
#             elif reply:
#                 at += reply
#             else:
#                 random = render_expression(EXPR_DONT_UNDERSTAND)
#                 at += random
#     else:
#         reply = await call_tuling_api(session, question)
#         if "图灵" in reply or "限制" in reply:
#             random = render_expression(EXPR_DONT_UNDERSTAND)
#             at += random
#         else:
#             at += reply
#     await session.send(at)


# async def test(message):
#     url = config.API
#     dic = dict()
#     dic['question'] = message
#     headers = {'Content-type': 'application/json'}
#     try:
#         r = requests.post(url, data=json.dumps(
#             dic), headers=headers, timeout=15000)
#         if r.status_code == 200:
#             data = r.json()
#             # results_list = data['k']
#             return data
#         else:
#             print("wrong,status_code: ", r.status_code)
#             return None
#     except Exception as e:
#         print(Exception, ' : ', e)
#         return None
