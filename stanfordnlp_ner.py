''' 创建stanfordnlp服务，并且对文本计算ner结果 '''
# usage: import
# author: luohuagang
# version: 0.0.1
# init: 7/11/2019
# last: 7/11/2019

from stanfordcorenlp import StanfordCoreNLP
import settings


class StanfordNER():
    ''' 调用stanfordnlp工具做ner
    '''
    def __init__(self, text):
        # 创建stanfordnlp工具，做ner
        nlp = StanfordCoreNLP(path_or_host=settings.stanfordnlp_host,
                              lang=settings.stanfordnlp_language,
                              port=settings.stanfordnlp_port)
        self.ner_result = nlp.ner(text)


if __name__ == "__main__":
    pass
