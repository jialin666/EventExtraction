''' 配置文件 '''
# author: luohuagang
# version: 0.0.1
# init: 6/26/2019
# last: 7/12/2019

HOST = 'http://localhost'
PORT = 5002
LANG = 'zh'

# 组织 地名
ORG = ['ORGANIZATION']
LOC = ['LOCATION', 'FACILITY', 'CITY', 'STATE_OR_PROVINCE', 'GPE']

# 火灾事件
FIRE_TRIGGER = {
    '火灾': '火灾事件',
    '爆炸': '火灾事件',
    }
FIRE_TIME = ['DATE', 'TIME', 'NUMBER', 'MISC']
FIRE_LOC = ['LOCATION', 'FACILITY', 'STATE_OR_PROVINCE']

# 金融事件
FINANCE_TRIGGER = {
    '裁员': '裁员事件',
    '警示函': '监管问询',
    '发行股份': '股票发行',
    }

# 参数相关消息
MSG_NO_PARSE = '入参必要字段为空'
MSG_ERROR_PARSE = '不支持的入参'
MSG_SUCCESS = '调用成功'
CODE_ERROR = 'ERROR'
CODE_SUCCESS = 'OK'
FUNC_LIST = ['ner', 'event', 'graph']
