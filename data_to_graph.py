# 将事件数据转化为图数据（节点和连接）
# author: luohuagang
# version: 0.0.1
# init: 6/26/2019
import copy

class DataToGraph():
    def __init__(self, event):
        self.graph = {}
        if event.event['events']:
            nodes = []
            links = []

            node = {}
            # 事件节点
            node['label'] = ''
            node['text'] = event.event['events']
            node['id'] = '100001'
            nodes.append(copy.deepcopy(node))

            # 触发词节点
            node['label'] = ''
            node['text'] = event.event['trigger']
            node['id'] = '200001'
            nodes.append(copy.deepcopy(node))

            # 事件时间节点
            if event.event['time']:
                node['label'] = ''
                node['text'] = event.event['time']
                node['id'] = '300001'
                nodes.append(copy.deepcopy(node))

            # 事件原因节点
            if event.event['cause']:
                node['label'] = ''
                node['text'] = event.event['cause']
                node['id'] = '600001'
                nodes.append(copy.deepcopy(node))

            # 事件位置节点
            if event.event['location']:
                node['label'] = ''
                node['text'] = '位置'
                node['id'] = '400001'
                nodes.append(copy.deepcopy(node))
                i = 0
                while i < len(event.event['location']):
                    node['label'] = ''
                    node['text'] = event.event['location'][i]
                    node['id'] = str(400002 + i)
                    nodes.append(copy.deepcopy(node))
                    i += 1

            # 事件组织节点
            if event.event['organization']:
                node['label'] = ''
                node['text'] = '救援组织'
                node['id'] = '500001'
                nodes.append(copy.deepcopy(node))
                i = 0
                while i < len(event.event['organization']):
                    node['label'] = ''
                    node['text'] = event.event['organization'][i]
                    node['id'] = str(500002 + i)
                    nodes.append(copy.deepcopy(node))
                    i += 1
            
            # 事件损失节点
            if event.event['lose']:
                node['label'] = ''
                node['text'] = '伤亡'
                node['id'] = '700001'
                nodes.append(copy.deepcopy(node))
                i = 0
                while i < len(event.event['lose']):
                    node['label'] = ''
                    node['text'] = event.event['lose'][i]
                    node['id'] = str(700002 + i)
                    nodes.append(copy.deepcopy(node))
                    i += 1

            link = {}
            # 事件 -- 触发词
            if event.event['trigger']:
                link['source'] = '100001'
                link['target'] = '200001'
                link['tag'] = '触发词'
                link['type'] = 'trigger'
                link['color'] = 'blue'
                links.append(copy.deepcopy(link))

            # 事件 -- 时间
            if event.event['time']:
                link['source'] = '100001'
                link['target'] = '300001'
                link['tag'] = '时间'
                link['type'] = 'time'
                link['color'] = 'blue'
                links.append(copy.deepcopy(link))

            # 事件 -- 地点
            if event.event['location']:
                link['source'] = '100001'
                link['target'] = '400001'
                link['tag'] = ''
                link['type'] = ''
                link['color'] = 'blue'
                links.append(copy.deepcopy(link))
                i = 0
                while i < len(event.event['location']):
                    link['source'] = '400001'
                    link['target'] = str(400002 + i)
                    link['tag'] = ''
                    link['type'] = ''
                    link['color'] = 'red'
                    links.append(copy.deepcopy(link))
                    i += 1

            # 事件 -- 救援组织
            if event.event['organization']:
                link['source'] = '100001'
                link['target'] = '500001'
                link['tag'] = ''
                link['type'] = ''
                link['color'] = 'blue'
                links.append(copy.deepcopy(link))
                i = 0
                while i < len(event.event['organization']):
                    link['source'] = '500001'
                    link['target'] = str(500002 + i)
                    link['tag'] = ''
                    link['type'] = ''
                    link['color'] = 'red'
                    links.append(copy.deepcopy(link))
                    i += 1

            # 事件 -- 原因
            if event.event['cause']:
                link['source'] = '100001'
                link['target'] = '600001'
                link['tag'] = '原因'
                link['type'] = 'cause'
                link['color'] = 'blue'
                links.append(copy.deepcopy(link))

            # 事件 -- 损失
            if event.event['lose']:
                link['source'] = '100001'
                link['target'] = '700001'
                link['tag'] = ''
                link['type'] = ''
                link['color'] = 'blue'
                links.append(copy.deepcopy(link))
                i = 0
                while i < len(event.event['lose']):
                    link['source'] = '700001'
                    link['target'] = str(700002 + i)
                    link['tag'] = ''
                    link['type'] = ''
                    link['color'] = 'red'
                    links.append(copy.deepcopy(link))
                    i += 1

            self.graph['nodes'] = nodes
            self.graph['links'] = links

