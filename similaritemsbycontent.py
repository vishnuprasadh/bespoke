import numpy as np
import nltk
import pandas as pd
import seaborn as sb
from sklearn import feature_extraction
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction import text
from sklearn.decomposition import PCA,TruncatedSVD
from nltk.stem.snowball import EnglishStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from logging.handlers import RotatingFileHandler
from math import *
from pandas import Series
import  re
import logging

import os


class similaritemsbycontent:
    logger = logging.getLogger("bespokelogger")
    logger.setLevel(logging.INFO)
    logger.addHandler(RotatingFileHandler("beskpokelog",'a',maxBytes=100000,backupCount=2))

    df = pd.DataFrame()
    articlevecors = pd.DataFrame()
    prodlist = list()
    similarityscore = dict()
    prod_title = None
    prod_content = None
    prod_bullets = None
    overall_prod_matrix = None
    consvalue = None
    overall_similarity_score = dict()


    def __init__(self):
        '''weigtage used'''
        self.most_similar = 1
        self.title_weight = 15
        self.subtitle_weight =25
        self.bullet_weight = 30
        self.overall_weight = 40




    def process(self):
        '''use title and bullets to group'''
        self._loadproductdata()
        self._applyidentifiers()
        dfmerged= self._vectorizeProducts()
        self._findsimilarproducts(dfmerged)



    def _findsimilarproducts(self,df):
        for index1, row1 in df.iterrows():
            simialrityscore =dict()
            for index2,row2 in df.iterrows():
                if index1 != index2:
                    simialrityscore[index2] = cosine_similarity(row1["coordinate"],row2["coordinate"])
            self.overall_similarity_score[index1] = simialrityscore
        print(self.overall_similarity_score)





    def _prepareframe(self,data):
        pass

    def _loadproductdata(self):
        dfprod = pd.read_csv(os.path.join(os.path.dirname(__file__), "stub/products1.csv"))
        self.df = dfprod[["bullets","categoryname","description","color","sizetitle","title","subtitle","productid"]]


    def _applyidentifiers(self):
        for index,row in self.df.iterrows():
            self.prodlist.append(row["productid"])

    def _vectorizeProducts(self):
        prodvectorizer = text.CountVectorizer()
        prodvectorize = self._vectorize()

        dfmerged = pd.DataFrame()
        dfmerged["productid"]= self.df["productid"]
        dfmerged["title"] = self.df["title"]
        dfmerged["info"] = pd.concat([self.df["title"].astype(str) + self.df["subtitle"].astype(str) +self.df["bullets"].astype(str)],axis=1,
                                                 join='inner')
        self.overall_prod_matrix = prodvectorize.fit_transform(dfmerged["info"])
        dfmerged["count"] = range(0,len(dfmerged))
        dfmerged["svd"] = self.overall_prod_matrix
        dfmerged["coordinate"] = dfmerged["count"].apply(lambda index: self.overall_prod_matrix[index,])

        dfmerged.drop("count",axis=1)
        dfmerged.to_csv("output.csv")

        self.overall_prod_matrix = self._reducedimensionality(self.overall_prod_matrix, features=self.overall_weight)

        return dfmerged
        '''
        self.prod_title = titlevectorize.fit_transform(self.df["title"])
        self.prod_title = self._reducedimensionality(self.prod_title, self.title_weight)
        #print(self.prod_title)
        self.prod_subtitle = titlevectorize.fit_transform(self.df["title"])
        self.prod_title = self._reducedimensionality(self.prod_subtitle, self.subtitle_weight)
        #print(self.prod_subtitle)
        self.prod_bullets = titlevectorize.fit_transform(self.df["bullets"])
        self.prod_title = self._reducedimensionality(self.prod_bullets, self.bullet_weight)
        #print(self.prod_bullets)
        self.prod_categoryname = titlevectorize.fit_transform(self.df["categoryname"])
        self.overall_prod_matrix = (self.prod_title,self.prod_subtitle,self.prod_bullets)
        self.consvalue = np.column_stack(self.prod_title,self.prod_subtitle,self.prod_bullets)
         '''


    def _vectorize(self):
        return self._getvectorizer()


    def _getvectorizer(self, ngram_range=(1,3),min_docfreq=2,max_docfreq=1.0):
        vectorizer = text.CountVectorizer(encoding='utf-8',lowercase=True,stop_words='english',min_df=min_docfreq,max_df=max_docfreq,
                                          analyzer="word",tokenizer=self.tokenizer,binary=True)

        return vectorizer


    def _reducedimensionality(self,data, features):
        reduced = TruncatedSVD(features,n_iter=2)
        data =reduced.fit_transform(data)
        data = np.array(data)
        return data



    @staticmethod
    def tokenizer(text):
        tokens = nltk.WhitespaceTokenizer().tokenize(text)
        '''replace all special chars'''
        tokens = [re.sub("^a-zA-Z\'","",token) for token in tokens]
        '''remove stopwords'''
        tokens = [word for word  in tokens if word not in stopwords.words('english')]
        stemmedwords = list()
        '''use stemmer to cleanup'''
        stemmer = SnowballStemmer("english")
        for token in tokens:
            token = stemmer.stem(token)
            if token != "": stemmedwords.append(token)
        return stemmedwords



if __name__ == '__main__':
    try:
        simitems = similaritemsbycontent()
        simitems.process()
    except Exception as ex:
        print(ex)