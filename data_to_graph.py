''' 将事件数据转化为图数据（节点和连接）'''
# author: luohuagang
# version: 0.0.1
# init: 6/26/2019
# last: 7/12/2019
import copy


def define_node(node_id, node_label, node_type):
    ''' 构造节点函数
    '''
    node = {}
    node['label'] = node_label
    node['id'] = node_id
    node['types'] = node_type
    return node

def define_link(start_node, end_node, link_label, link_type):
    ''' 构造连接函数
    '''
    link = {}
    link['source'] = start_node
    link['target'] = end_node
    link['label'] = link_label
    link['type'] = link_type
    return link


class DataToGraph():
    ''' 将事件信息转化为图信息
    '''
    def __init__(self, event):
        ''' 初始化
        '''
        self.event = event
        self.graph = {}

        self.nodes = []
        self.links = []

        if self.event.event['事件']:
            self.normal_graph()

        self.graph['nodes'] = self.nodes
        self.graph['links'] = self.links


    def normal_graph(self):
        ''' 通用的生成函数
        '''
        parent_id = 10000
        node_id = 20000
        node = define_node(str(parent_id), self.event.event['事件'], '事件')
        self.nodes.append(copy.deepcopy(node))

        for item_key, item_value in self.event.event.items():
            if item_key == '事件':
                continue
            if isinstance(item_value, str):
                node = define_node(str(node_id), item_value, item_key)
                self.nodes.append(copy.deepcopy(node))
                link = define_link(str(parent_id), str(node_id), item_key, '')
                self.links.append(copy.deepcopy(link))
            elif isinstance(item_value, list):
                if not item_value:
                    continue
                node = define_node(str(node_id), item_key, item_key)
                self.nodes.append(copy.deepcopy(node))
                link = define_link(str(parent_id), str(node_id), '', '')
                self.links.append(copy.deepcopy(link))
                child_id = node_id
                for item in item_value:
                    child_id += 1
                    node = define_node(str(child_id), item, item_key)
                    self.nodes.append(copy.deepcopy(node))
                    link = define_link(str(node_id), str(child_id), '', '')
                    self.links.append(copy.deepcopy(link))
            else:
                continue
            node_id += 10000
