import numpy as np
from scipy.spatial.distance import correlation
from scipy.stats import pearsonr
import pandas as pd
import logging
from eventcontext import context
from pandas import tseries
from logging.handlers import RotatingFileHandler
from datetime import datetime

import os

class recommender:
    dfprod = pd.DataFrame()
    dforder = pd.DataFrame()
    dfcustprodmatrix = pd.DataFrame()

    logger = logging.getLogger("bespoke")
    logger.setLevel(logging.INFO)
    logger.handlers.append(RotatingFileHandler("recommender.log","a",1000000,2))

    def __init__(self):
        self.logger.info("Time started is {}".format(datetime.now().strftime("%d-%m-%Y %H:%M:%S")))
        prodfile = os.path.join(os.path.dirname(__file__),"stub/products.csv")
        orderfile = os.path.join(os.path.dirname(__file__),"stub/customerorder.csv")
        self.dfprod = pd.read_csv(prodfile,header=0, encoding='ISO-8859-1') #names=["productid","categoryid","categoryname","brand"])#names=["brand","categoryid","categoryname","color","productid"])
        self.dforder = pd.read_csv(orderfile,header=0,encoding='ISO-8859-1')#names=["customerid","productid","ordereddate"])
        self._createcustomerorderpivot()
        self.logger.info("Init completed, loading the products & customers")

    def _createcustomerorderpivot(self):
        self.dfmergedprodcust = pd.merge(self.dfprod,self.dforder,how="outer",on="productid")
        logging.info("Customerprod generated successfully")
        self.dfcustprodmatrix = pd.pivot_table(self.dfmergedprodcust,index="customerid",columns="productid",values="qty"
                                            )
        print(self.dfcustprodmatrix.head())
        self.logger.info("userproduct pivot created and has {} rows".format(len(self.dfcustprodmatrix)))

        dfcust = self.dforder["customerid"].unique()

        for row in dfcust:
            self._nearestneighbours(row,5)


    def _similaritybeweenusers(self,user1,user2):
        '''Mean is not required as the way we have built logic is 0 or 1 i.e binary representation against product'''
        user11 = np.array(user1) #- np.mean(user1)
        user22 = np.array(user2) #- np.mean(user2)
        '''find products which both have purchased'''
        commonbought=[]

        for prod in range(len(user11)):
            if user11[prod] > 0 and user22[prod] > 0: commonbought.append(prod)
        #commonbought = [i for i in range(len(user1)) if user1[i] >0 and user2[i] > 0 ]

        if len(commonbought) == 0:
            return  0
        else:
            user1 = np.array([user11[i] for i in commonbought])
            user2 = np.array([user22[i] for i in commonbought])
            print("Pearsoncoeff is {}".format(pearsonr(user1,user2)))
            print("numpy coeff is {}".format(np.correlate(user1,user2)))
            print("scipymetrics coeff is {}".format(correlation(user1, user2)))
            return correlation(user1,user2)

    def _nearestneighbours(self,activeuser,K):
        similaritymatrix = pd.DataFrame()
        similaritymatrix = pd.DataFrame(index = self.dfcustprodmatrix.index, columns=['similarity'])
        #lists all the users with empty similarity dataframe.
        for index in self.dfcustprodmatrix.index:
            #We need to skip where index value is same as user
            if index != activeuser:
                simlarityscore = self._similaritybeweenusers(self.dfcustprodmatrix.loc[activeuser],
                                                                      self.dfcustprodmatrix.loc[index])
                self.logger.info("Similarity score for {} and {} is {}".format(activeuser,index,simlarityscore))
                similaritymatrix.loc[index] = simlarityscore
            #finds similarity b/w activeuser and user in customermatrix index. This will iterate similarity
            # the activeuser and all other users.
        similaritymatrix = pd.DataFrame.sort_values(similaritymatrix,['similarity'],ascending=[0])
        #now we get the top K users who are closest to the activeusers.
        nearestneighbors = similaritymatrix[:K]

        print("Active user - {} nearest neighbors are {}".format(np.array(nearestneighbors).astype(str)))

        #neighborcustprodmatrix = self.dfcustprodmatrix.loc[nearestneighbors.index]
        # this picks and assigns all users who are closest.
        #print(nearestneighbors)

        #predicteditem = pd.DataFrame(index =self.dfcustprodmatrix.columns,columns=['users'])
        #for col in self.dfcustprodmatrix.columns:



    def _recommendforuser(self,userid,productid):
        pass

rec = recommender()
