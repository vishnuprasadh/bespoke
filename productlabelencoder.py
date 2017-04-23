import logging
from logging.handlers import RotatingFileHandler
from sklearn import preprocessing
import pandas as pd
import numpy as np
from collections import defaultdict
from sklearn.feature_selection import SelectKBest
from configuration import configuration
import json
from json import dumps
from kafka import KafkaClient
from kafkautility import kafkafactory

'''
This is an encoder for product which will encode the fields with labels where there are discrete variables.
The encoder has predefined logic for the same. It has list of columns which are core and which are feature based which means may or may not exist.
All the core ones are reviewed and normalized in 0,1,2,3 formats.
All the feature ones also are normalized
Core    : "brand","style","material","size","weight","colour","color","age","agerange"
feature : "pattern","sleeve","occassion"

Missing value treatment : In case of core or feature a value of -1 is entered for missing ones and then labelencoded. 
We will improve this for better imputation or evaluation later.

Any columns other than that are ignored and just cleared up for missing values or na's.
'''
class encoder(object):

    '''list all the columns from core and feature which need encoding. Ensure all are in lower case'''
    core_columns_toencode = ["brand","style","material","size","weight","colour","color","age","agerange"]
    feature_columns_toencode =["pattern","sleeve","occassion"]
    consolidated_columns = dict()

    df = pd.DataFrame()
    dfcopy = pd.DataFrame()

    logger = logging.getLogger("bespoke")
    handler = RotatingFileHandler("bespoke.log", mode="a", maxBytes=500000, backupCount=5)

    def __init__(self):
        if not self.logger.handlers:
            self.logger.addHandler(self.handler)


    '''Pass the Dataframe input which will return the final LabelEncoded & normalized data'''
    def getpreprocessandcleanupdata(self,dfinput=None,stream=False):

        '''if not given'''
        if not dfinput:
            #dfinput = pd.read_csv('../DataSets/Sampleitem.csv', sep=",", header=0)
            kf = kafkafactory()
            kf.readmessage(kafkafactory.MessageType.Test)
            # print(dfinput["style"].describe())
            dfinput = self._returndata(dfinput)

        if stream == True:
            pass




        dftrain = dfinput[1:12]
        dftest = dfinput[13:]
        print(dftrain)
        print(dftest)



        #print(dfinput["style"].describe())

        '''labelencode and send'''
        #return self._returndata(dfinput)
        #return 0

    '''Just an aggregate function which calls the labelencoder, normalization functions and returns final dataframe'''
    def _returndata(self,dfinput):

        dfcopy = dfinput.copy()
        self.dfcopy = self._getlabelencodeproductfeed(dfinput,dfcopy)
        self._normalizeproductfeed()
        return self.dfcopy

    '''Pass both the original dataframe and the copy of the dataframe which will labelEncode the copy and return the copied dataframe'''
    def _getlabelencodeproductfeed(self,df,dfcopy):
        lencode = preprocessing.LabelEncoder()

        '''In each column loop through'''
        for k in df.columns:
            #print("Column name is {}".format(k))

            '''Here am going through all feature columns where we have asked for encoding and encoding them'''
            if (str(k).lower() in self.feature_columns_toencode):
                self.consolidated_columns[k]="feature"
                print("core feature - {}".format(k))
                '''I will provide a -1 where the values are missing'''
                #coldata = pd.Series(dfcopy,dfcopy[k].index)
                #print(coldata)
                print( dfcopy[k])
                dfcopy[k].fillna("-1",inplace=True)
                dfcopy[k] = lencode.fit_transform(dfcopy[k])

            elif (str(k).lower() in self.core_columns_toencode):
                '''Here am going through all core columns where we have asked for encoding and encoding them'''
                '''also if there are core columns which are core but need encoding'''
                if  k in self.core_columns_toencode:
                    '''first fill the missing columns from core with the value'''
                    dfcopy[k].fillna("-1", inplace=True)
                    '''next i do label transform'''
                    dfcopy[k] = lencode.fit_transform(dfcopy[k])
                    self.consolidated_columns[k] = "core"
            else:
                '''Here am anyway marking other items as part of others and saving them in consolidated columns list'''
                self.consolidated_columns[k] = "others"
                dfcopy[k].fillna(k,inplace=True)

        return dfcopy

    '''In this method we will normalize'''
    def _normalizeproductfeed(self):
        pass


if __name__ == '__main__':
    '''# Test program'''
    e = encoder()
    df = e.getpreprocessandcleanupdata()
    #print(df.head())