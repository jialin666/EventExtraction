''' 事件抽取  '''
# usage: import
# author: luohuagang
# version: 0.0.1
# init: 6/25/2019
# last: 7/10/2019

import re
import settings


class EventExtraction():
    ''' 事件提取类
    '''
    def __init__(self, context, nlp):
        # 初始化事件字典，包含触发词，事件类型
        # 时间，地点，救援组织，事故原因，事故损失
        self.nlp_result = nlp.ner_result
        self.news = context
        self.event = {}

        self.having_event()

        if self.event['触发词'] in settings.FIRE_TRIGGER:
            self.fire_event()
        elif self.event['触发词'] == '警示函':
            self.finance_punishment()
        elif self.event['触发词'] == '裁员':
            self.finance_loyaffs()
        elif self.event['触发词'] == '发行股份':
            self.finance_lssuing()

    def fire_event(self):
        ''' 火灾事件
        '''
        # 提取时间、地点、救援组织
        self.event['火灾时间'] = self.taking_time()[0]
        self.event['火灾地点'] = self.taking_location()
        self.event['救援组织'] = self.taking_organization()
        # 匹配事故原因和事故损失
        self.cause = pattern_match(pattern_cause(), self.news)
        self.lose = pattern_match(pattern_lose(), self.news)
        self.event['火灾原因'] = "".join(self.cause)
        self.event['伤亡损失'] = self.lose

    def finance_loyaffs(self):
        ''' 裁员事件
        '''
        event_time = self.taking_time()
        if event_time:
            self.event['时间'] = event_time[0]
        self.event['裁员组织'] = self.taking_organization()
        self.event['裁员人数'] = self.taking_number()

    def finance_punishment(self):
        ''' 处罚事件
        '''
        event_time = self.taking_time()
        if event_time:
            self.event['时间'] = event_time[0]
        organizations = self.taking_organization()
        if organizations:
            self.event['监管组织'] = []
            self.event['受罚组织'] = []
        for organization in organizations:
            if re.search(re.compile(r"证监会"), organization):
                self.event['监管组织'].append(organization)
            elif re.search(re.compile(r"证监局"), organization):
                self.event['监管组织'].append(organization)
            else:
                self.event['受罚组织'].append(organization)

    def finance_lssuing(self):
        ''' 发行股票事件
        '''
        event_time = self.taking_time()
        if event_time:
            self.event['时间'] = event_time[0]
        self.event['发行组织'] = self.taking_organization()
        numbers = self.taking_number()
        for number in numbers:
            if re.search(r"[\d.]*?万", number):
                self.event['发行量'] = number
            if re.search(r"[\d.]*?元", number):
                self.event['发行价格'] = number
        number = re.search(r"([\d万]+?股)", self.news)
        if number:
            self.event['发行量'] = number[0]

    def having_event(self):
        ''' 获取事件
        '''
        for item in self.nlp_result:
            if item[1] == 'CAUSE_OF_DEATH':
                if item[0] in settings.FIRE_TRIGGER:
                    self.event['触发词'] = item[0]
                    self.event['事件'] = settings.FIRE_TRIGGER[item[0]]
                    return

        finance_trigger = [key for key in settings.FINANCE_TRIGGER]
        re_pattern = re.compile(r"({})".format('|'.join(finance_trigger)))
        match_list = re.findall(re_pattern, self.news)
        if match_list:
            self.event['触发词'] = match_list[0]
            self.event['事件'] = settings.FINANCE_TRIGGER[match_list[0]]
            return

        # 未发现触发词
        self.event['事件'] = None
        self.event['触发词'] = None

    def taking_number(self):
        ''' 获取数目
        '''
        i = 0
        state = False
        having_time = False
        only_number = True
        number = ""
        result = []
        while i < len(self.nlp_result):
            if self.nlp_result[i][1] in ['DATE', 'TIME']:
                having_time = True
            elif self.nlp_result[i][1] in ['NUMBER']:
                number += self.nlp_result[i][0]
                state = True
            elif self.nlp_result[i][1] in ['PERCENT', 'MONEY']:
                number += self.nlp_result[i][0]
                state = True
                only_number = False
            elif self.nlp_result[i][1] == 'MISC':
                number += self.nlp_result[i][0]
                only_number = False
            else:
                if state and not having_time and not only_number:
                    result.append(number)
                number = ""
                state = False
                having_time = False
                only_number = True
            i += 1
        if state and not having_time and not only_number:
            result.append(number)

        result = list(set(result))
        return result

    def taking_time(self):
        ''' 获取时间
        '''
        i = 0
        state = False
        time_fire = ""
        result = []
        while i < len(self.nlp_result):
            if self.nlp_result[i][1] in ['DATE', 'TIME']:
                time_fire += self.nlp_result[i][0]
                state = True
            elif self.nlp_result[i][1] in ['NUMBER', 'MISC']:
                time_fire += self.nlp_result[i][0]
            else:
                if state:
                    result.append(time_fire)
                time_fire = ""
                state = False
            i += 1
        if state:
            result.append(time_fire)

        return result


    def taking_location(self):
        ''' 获取地点
        '''
        i = 0
        state = False
        location = ""
        result = []
        while i < len(self.nlp_result):
            if (self.nlp_result[i][1] == 'LOCATION' or
                    self.nlp_result[i][1] == 'FACILITY' or
                    self.nlp_result[i][1] == 'CITY'):
                location += self.nlp_result[i][0]
                if not state:
                    state = True
            else:
                if state:
                    result.append(location)
                    location = ""
                    state = False
            i += 1
        if state:
            result.append(location)

        result = list(set(result))

        return result


    def taking_organization(self):
        ''' 获取组织
        '''
        i = 0
        state = False
        organization = ""
        result = []
        while i < len(self.nlp_result):
            if self.nlp_result[i][1] in settings.ORG:
                organization += self.nlp_result[i][0]
                if not state:
                    state = True
            else:
                if state:
                    result.append(organization)
                    organization = ""
                    state = False
            i += 1
        if state:
            result.append(organization)

        result = list(set(result))

        return result


def pattern_match(patterns, text):
    ''' 匹配给定模板，返回匹配列表
    '''
    result = []

    for pattern in patterns:
        match_list = re.findall(pattern, text)
        if match_list:
            result.append(match_list[0])
    return result


def pattern_cause():
    ''' 事故原因提取模板
    '''
    patterns = []

    key_words = ['起火', '事故', '火灾']
    pattern = re.compile('.*?(?:{0})原因(.*?)[,.?:;!，。？：；！]'.format('|'.join(key_words)))
    patterns.append(pattern)

    return patterns


def pattern_lose():
    ''' 定义损失模板
    '''
    patterns = []

    key_words = ['伤亡', '损失']
    pattern = re.compile('.*?(未造成.*?(?:{0}))[,.?:;!，。？：；]'.format('|'.join(key_words)))
    patterns.append(pattern)

    patterns.append(re.compile(r'(\d+人死亡)'))
    patterns.append(re.compile(r'(\d+人身亡)'))
    patterns.append(re.compile(r'(\d+人受伤)'))
    patterns.append(re.compile(r'(\d+人烧伤)'))
    patterns.append(re.compile(r'(\d+人坠楼身亡)'))
    patterns.append(re.compile(r'(\d+人遇难)'))

    return patterns


if __name__ == '__main__':
    pass
