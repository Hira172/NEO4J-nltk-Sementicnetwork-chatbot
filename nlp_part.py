from nltk import  word_tokenize,pos_tag
from ML import model
class nlp_part:
    def __init__(self):
        self.nnModel = model('mldatasets/NNDataset.csv')
        self.nnModel.train()
        self.nnpModel = model('mldatasets/NNPDataset.csv')
        self.nnpModel.train()
        self.jjModel = model('mldatasets/JJDataset.csv')
        self.jjModel.train()
        self.cdModel = model('mldatasets/CDDataset.csv')
        self.cdModel.train()
    # sentence = 'Hamza have 4 cat'
    def processData(self,sentence):
        # print(self.nnModel)
        tokens = word_tokenize(sentence)
        postTaggedList  = pos_tag(tokens)
        print(postTaggedList)
        noun = []
        verb = []
        adjective = []
        IN= []
        count = 0
        CC = []
        for tuple in postTaggedList:
            # print(tuple[0], ": ", tuple[1])
            if tuple[1] == 'NNP'  or tuple[1] == 'NNPS':
                noun.append((tuple[0],self.nnpModel.predict(tuple[0])))
            if  tuple[1] == 'NNS'  or tuple[1] == 'NN':
                noun.append((tuple[0], self.nnModel.predict(tuple[0])))
            if tuple[1] == 'VBZ' or tuple[1] == 'VB' or tuple[1] == 'VBD' or tuple[1] == 'VBD' or tuple[1] == 'VBG' or tuple[1] == 'VBN' or tuple[1] == 'VBP':
                verb.append(tuple[0])
            if tuple[1] == 'JJ' or tuple[1] == 'JJS':
                adjective.append((tuple[0],self.jjModel.predict(tuple[0])))
            if tuple[1] == 'CD':
                count = (tuple[0],self.cdModel.predict(tuple[0]))
            if tuple[1] == 'IN':
                IN.append(tuple[0])
            if tuple[1] == 'CC':
                CC.append(tuple[0])
        # print("noun:",noun,"verb:", verb,"adjective", adjective,"number", count)
        return  noun, verb, adjective, count,IN,CC
# n=nlp_part()
# sentence = "Hira is a girl"
# print(n.processData(sentence))