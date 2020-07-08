# HITszQAbot

[![996.icu](https://img.shields.io/badge/link-996.icu-red.svg)](https://996.icu)

## 简介

招生咨询信息问答系统是基于深度学习文本分类算法，面向招生信息咨询的 QQ 问答机器人。

## 项目结构

```none
├── faq # nonebot 框架
│	└── plugins
│		├── faq
│		│	└── __init__.py # 群问答插件
│		├── txt_tools.py # 文本处理工具
│		└── welcome.py # 群欢迎插件
├── config.py # 配置文件
├── faqbot.py # 启动
└── nlp_module # 文本分类网络
│	├── pytorch_pretrained 
│	├── ERNIE_pretrain
│	├── models 
│	│	└── bert.py # 模型
│	├── RequestHandler.py # 调用模型
│	├── run.py # 训练模型
│	├── train_eval.py # 训练过程
│	├── utils.py # 原数据处理
│	└── utils_new.py # 数据处理工具
└── environment.yml # 通过 conda 生成的项目依赖文件
```

## 环境配置

### 方法一：通过 Anaconda 配置

假设已经安装了 Anaconda，并 clone 本仓库到本地，那么打开 cmd，输入以下命令：

```
$ cd <项目位置>
$ conda env create -f environment.yml
```

耐心等待，配置速度取决于网络环境。

### 方法二：通过 pip 配置（不推荐）

python 版本 3.6

打开 cmd，输入以下命令：

```
$ cd <项目位置>
$ pip install -r requirements.txt
```

注：建议使用虚拟环境

## 数据

数据文件：.bot/nn/data/train.txt

数据格式：question+'\t'+'\_label\_'+label

将处理好的数据放入 .bot/nn/data 中替换 train.txt

## 训练

请移步至此项目：

https://github.com/L-M-Sherlock/Bert-Chinese-Text-Classification-Pytorch

## 预测

预测 label：python RequestHandler.py

将需要分类的 question 放入 rh_sub.get_result('分类句子') 中运行，得到分类结果

## 部署

1. 配置 ./config.py 文件
2. 下载安装[酷 Q](https://cqp.cc/) 并登入 QQ
3. 安装插件 [CoolQ HTTP API](https://cqhttp.cc/)
4. 配置 ..\酷Q Air\data\app\io.github.richardchien.coolqhttpapi\config\\*.json 文件
5. 重启酷 Q
6. 运行：python faqbot.py

更多关于酷 Q 机器人的开发与使用请参见：[基于 酷Q 的 Python 异步 QQ 机器人框架](https://nonebot.cqp.moe/)