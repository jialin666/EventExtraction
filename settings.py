# 配置文件
# author: luohuagang
# version: 0.0.1
# init: 6/26/2019
# last: 6/26/2019

stanfordnlp_host = 'http://localhost'
stanfordnlp_port = 5002
stanfordnlp_language = 'zh'

test_data_path = '/home/luohuagang/project/my_github/EventExtraction/data/test_fire_news'

# 火灾事件
trigger_fire = ['火灾', '爆炸']
time_fire = ['DATE', 'TIME', 'NUMBER', 'MISC']
location_fire = ['LOCATION', 'FACILITY', 'STATE_OR_PROVINCE']
organization_fire = ['ORGANIZATION']

# 金融事件

# 参数相关消息
MSG_NO_PARSE = '入参必要字段为空'
MSG_ERROR_PARSE = '不支持的入参'
MSG_SUCCESS = '调用成功'
CODE_ERROR = 'ERROR'
CODE_SUCCESS = 'OK'
FUNC_LIST = ['ner', 'event', 'graph']
