from os import path

import nonebot

import config as config

if __name__ == '__main__':
    nonebot.init(config)
    print('1')
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'faq', 'plugins'),
        'faq.plugins',
    )
    print('2')
    nonebot.run()
    print('3')
