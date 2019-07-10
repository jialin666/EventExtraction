"""
# 搭建rest服务
# author: luohuagang
# version: 0.0.2
# date: 6/25/2019
"""
import time
from flask import Flask, jsonify, request
from event_extraction import EventExtraction
from data_to_graph import DataToGraph
from ner import NER


SERVICE = Flask(__name__)

MSG_NO_PARSE = '入参必要字段为空'
MSG_ERROR_PARSE = '不支持的入参'
MSG_SUCCESS = '调用成功'
CODE_ERROR = 'ERROR'
CODE_SUCCESS = 'OK'
FUNC_LIST = ['ner', 'event', 'graph']


@SERVICE.route('/mas/rest/fire/v1',
               methods=['POST'])
def eventextraction_v1():
    ''' 事件提取
    '''
    result = {}

    result['code'] = 'OK'
    result['msg'] = '调用成功'
    result['timestamp'] = str(int(time.time()))

    json_data = request.get_json()
    news = json_data['body']['text']
    event = EventExtraction(news)

    result['body'] = {}
    result['body']['graph'] = DataToGraph(event).graph
    result['body']['event_extraction'] = event.event

    return jsonify(result)


@SERVICE.route('/mas/rest/fire/v1_2',
               methods=['POST'])
def eventextraction_v1_2():
    ''' 火灾事件提取v1.2版服务
    '''
    json_data = request.get_json()
    result = {}

    # 处理入参
    if 'app_key' in json_data:
        if json_data['app_key'] != 'masweb_demo':
            result['code'] = CODE_ERROR
            result['msg'] = MSG_ERROR_PARSE + \
                            ': app_key is {}.'.format(json_data['app_key'])
            result['time'] = str(int(time.time()))
            return jsonify(result)
    else:
        result['code'] = CODE_ERROR
        result['msg'] = MSG_NO_PARSE + ': app_key'
        result['time'] = str(int(time.time()))
        return jsonify(result)

    if 'func' in json_data:
        for func in json_data['func']:
            if func not in FUNC_LIST:
                result['code'] = CODE_ERROR
                result['msg'] = MSG_ERROR_PARSE + \
                                ': {} in func'.format(func)
                result['time'] = str(int(time.time()))
                return jsonify(result)
    else:
        result['code'] = CODE_ERROR
        result['msg'] = MSG_NO_PARSE + ': func'
        result['time'] = str(int(time.time()))
        return jsonify(result)

    news = json_data['body']['text']

    # 参数检测通过，则调用成功
    result['code'] = CODE_SUCCESS
    result['msg'] = MSG_SUCCESS
    result['timestamp'] = str(int(time.time()))

    result['body'] = {}

    event = EventExtraction(news)
    # 根据func定义返回内容
    if 'ner' in json_data['func']:
        result['body']['ner'] = NER(event).ner

    if 'event' in json_data['func']:
        result['body']['event_extraction'] = event.event

    if 'graph' in json_data['func']:
        result['body']['graph'] = DataToGraph(event).graph

    return jsonify(result)


def main():
    ''' main 函数
    '''
    SERVICE.config['JSON_AS_ASCII'] = False
    SERVICE.run(
        host='0.0.0.0',
        port=5001,
        debug=True
    )


if __name__ == '__main__':
    main()
