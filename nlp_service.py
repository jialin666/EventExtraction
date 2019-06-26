"""
# 搭建rest服务
# author: luohuagang
# version: 0.0.1
# date: 6/25/2019
"""

from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from stanfordcorenlp import StanfordCoreNLP
from event_extraction import EventExtraction
from data_to_graph import DataToGraph
import time
import json


app = Flask(__name__)
api = Api(app)


class NLPService(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        
        parser.add_argument('app_key', type=str)
        parser.add_argument('app_version', type=str)
        parser.add_argument('timestamp', type=str)
        parser.add_argument('func', type=str)
        parser.add_argument('language', type=str)
        parser.add_argument('body')

        args = parser.parse_args()

        result = {}
        result['code'] = 'OK'
        result['msg'] = '调用成功'
        result['timestamp'] = str(time.time())
        
        nlp = StanfordCoreNLP('http://localhost', port=5002)
        body = eval(args['body'])
        text = body['text']
        props = {
            'annotators': args['func'],
            'pipelineLanguage': args['language'],
            'outputFormat': 'json'
        }
        nlp_result = nlp.annotate(text, properties=props)
        result['body'] = json.loads(nlp_result)
        nlp.close()
 
        #result = json.dumps(result, ensure_ascii=False)

        return result

class EventExtractionService(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        
        parser.add_argument('app_key', type=str)
        parser.add_argument('app_version', type=str)
        parser.add_argument('timestamp', type=str)
        parser.add_argument('body')

        args = parser.parse_args()

        result = {}
        
        
        result['code'] = 'OK'
        result['msg'] = '调用成功'
        result['timestamp'] = str(time.time())
        
        body = eval(args['body'])
        text = body['text']
        event = EventExtraction(text)

        result['body'] = {}
        result['body']['graph'] = DataToGraph(event).graph
        result['body']['event_extraction'] = event.event
        
        #result['body'] = event.event

        return result


api.add_resource(NLPService, '/mas/rest/stanfordnlp/v1')
api.add_resource(EventExtractionService, '/mas/rest/eventextraction/v1')

if __name__=='__main__':
    app.run(
      host='0.0.0.0',
      port=5001,
      debug=True
    )

