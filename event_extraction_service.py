"""
# 搭建rest服务
# author: luohuagang
# version: 0.0.3
# date: 6/25/2019
# last: 7/11/2019
"""
import time
from flask import Flask, jsonify, request

import settings
from event_extraction import EventExtraction
from data_to_graph import DataToGraph
from ner import NER
from stanfordnlp_ner import StanfordNER

SERVICE = Flask(__name__)


@SERVICE.route('/mas/rest/fire/v1', methods=['POST'])
def eventextraction_v1():
    ''' 事件提取
    '''
    result = {}

    result['code'] = 'OK'
    result['msg'] = '调用成功'
    result['timestamp'] = str(int(time.time()))

    json_data = request.get_json()
    news = json_data['body']['text']

    nlp = StanfordNER(news)
    event = EventExtraction(news, nlp)

    result['body'] = {}
    result['body']['graph'] = DataToGraph(event).graph
    result['body']['event_extraction'] = event.event

    return jsonify(result)


@SERVICE.route('/mas/rest/fire/v1_2', methods=['POST'])
def eventextraction_v1_2():
    ''' 火灾事件提取v1.2版服务
    '''
    json_data = request.get_json()
    result = {}

    # 处理入参
    if 'app_key' in json_data:
        if json_data['app_key'] != 'masweb_demo':
            result['code'] = settings.CODE_ERROR
            result['msg'] = settings.MSG_ERROR_PARSE + \
                            ': app_key is {}.'.format(json_data['app_key'])
            result['time'] = str(int(time.time()))
            return jsonify(result)
    else:
        result['code'] = settings.CODE_ERROR
        result['msg'] = settings.MSG_NO_PARSE + ': app_key'
        result['time'] = str(int(time.time()))
        return jsonify(result)

    if 'func' in json_data:
        for func in json_data['func']:
            if func not in settings.FUNC_LIST:
                result['code'] = settings.CODE_ERROR
                result['msg'] = settings.MSG_ERROR_PARSE + \
                                ': {} in func'.format(func)
                result['time'] = str(int(time.time()))
                return jsonify(result)
    else:
        result['code'] = settings.CODE_ERROR
        result['msg'] = settings.MSG_NO_PARSE + ': func'
        result['time'] = str(int(time.time()))
        return jsonify(result)

    news = json_data['body']['text']

    # 参数检测通过，则调用成功
    result['code'] = settings.CODE_SUCCESS
    result['msg'] = settings.MSG_SUCCESS
    result['timestamp'] = str(int(time.time()))

    result['body'] = {}

    nlp = StanfordNER(news)
    # 根据func定义返回内容
    if 'ner' in json_data['func']:
        result['body']['ner'] = NER(nlp).ner

    if 'event' in json_data['func']:
        event = EventExtraction(news, nlp)
        result['body']['event_extraction'] = event.event
        if 'graph' in json_data['func']:
            result['body']['graph'] = DataToGraph(event).graph

    return jsonify(result)


@SERVICE.route('/mas/rest/finance/v1', methods=['POST'])
def eventextraction_finance_v1():
    ''' 火灾事件提取v1.2版服务
    '''
    json_data = request.get_json()
    result = {}

    # 处理入参
    if 'app_key' in json_data:
        if json_data['app_key'] != 'masweb_demo':
            result['code'] = settings.CODE_ERROR
            result['msg'] = settings.MSG_ERROR_PARSE + \
                            ': app_key is {}.'.format(json_data['app_key'])
            result['time'] = str(int(time.time()))
            return jsonify(result)
    else:
        result['code'] = settings.CODE_ERROR
        result['msg'] = settings.MSG_NO_PARSE + ': app_key'
        result['time'] = str(int(time.time()))
        return jsonify(result)

    if 'func' in json_data:
        for func in json_data['func']:
            if func not in settings.FUNC_LIST:
                result['code'] = settings.CODE_ERROR
                result['msg'] = settings.MSG_ERROR_PARSE + \
                                ': {} in func'.format(func)
                result['time'] = str(int(time.time()))
                return jsonify(result)
    else:
        result['code'] = settings.CODE_ERROR
        result['msg'] = settings.MSG_NO_PARSE + ': func'
        result['time'] = str(int(time.time()))
        return jsonify(result)

    news = json_data['body']['text']

    # 参数检测通过，则调用成功
    result['code'] = settings.CODE_SUCCESS
    result['msg'] = settings.MSG_SUCCESS
    result['timestamp'] = str(int(time.time()))

    result['body'] = {}

    nlp = StanfordNER(news)
    # 根据func定义返回内容
    if 'ner' in json_data['func']:
        result['body']['ner'] = NER(nlp).ner

    if 'event' in json_data['func']:
        event = EventExtraction(news, nlp)
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
        port=5003,
        debug=True
    )


if __name__ == '__main__':
    main()
