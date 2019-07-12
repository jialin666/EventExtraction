''' ner '''
# -*-encoding:utf-8-*-


import settings


class NER():
    ''' 处理ner结果，返回时间、地名、组织
    '''
    def __init__(self, nlp):
        self.nlp_result = nlp.ner_result
        self.ner = {}
        self.ner['time'] = self.taking_time()
        self.ner['location'] = self.taking_location()
        self.ner['organization'] = self.taking_organization()
        self.ner['number'] = self.taking_number()

    def taking_time(self):
        ''' 获取时间
        '''
        i = 0
        state = False
        only_number = True
        time_fire = ""
        result = []
        while i < len(self.nlp_result):
            if self.nlp_result[i][1] in ['DATE', 'TIME']:
                time_fire += self.nlp_result[i][0]
                if not state:
                    state = True
                    only_number = False
            elif self.nlp_result[i][1] == 'NUMBER':
                time_fire += self.nlp_result[i][0]
                if not state:
                    state = True
            elif self.nlp_result[i][1] == 'MISC':
                time_fire += self.nlp_result[i][0]
            else:
                if state and not only_number:
                    result.append(time_fire)
                time_fire = ""
                state = False
                only_number = True
            i += 1
        if state:
            result.append(time_fire)

        result = list(set(result))

        return result

    def taking_location(self):
        ''' 获取地点
        '''
        i = 0
        state = False
        location = ""
        result = []
        while i < len(self.nlp_result):
            if self.nlp_result[i][1] in settings.LOC:
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

    def taking_number(self):
        ''' 获取数目
        '''
        i = 0
        state = False
        having_time = False
        number = ""
        result = []
        while i < len(self.nlp_result):
            if self.nlp_result[i][1] in ['DATE', 'TIME']:
                number += self.nlp_result[i][0]
                if not state:
                    state = True
                    having_time = True
            elif self.nlp_result[i][1] in ['NUMBER', 'PERCENT', 'MONEY']:
                number += self.nlp_result[i][0]
                if not state:
                    state = True
            elif self.nlp_result[i][1] == 'MISC':
                number += self.nlp_result[i][0]
            else:
                if state and not having_time:
                    result.append(number)
                number = ""
                state = False
                having_time = False
            i += 1
        if state:
            result.append(number)

        result = list(set(result))

        return result


if __name__ == '__main__':
    pass
