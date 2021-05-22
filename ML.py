import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction import DictVectorizer
from  sklearn.tree import DecisionTreeClassifier

class model():
    def __init__(self,path):
        self.path = path
        self.cv = CountVectorizer()
        self.tree = DecisionTreeClassifier()

    def train(self):
        df_data = pd.read_csv(self.path)
        Xfeatures = df_data['Word']
        y = df_data['Type']
        X = self.cv.fit_transform(Xfeatures)
        self.tree.fit(X,y)
        # print("Accuracy of Decision Tree  on test dataset",self.tree.score(X,y)*100,"%")

    def predict(self,word):
        vector = self.cv.transform([word]).toarray()
        res = self.tree.predict(vector)
        # print( res[0])
        return res[0]
# print(model('dataset'))