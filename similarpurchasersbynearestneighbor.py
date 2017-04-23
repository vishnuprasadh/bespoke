import numpy as np
from scipy.stats import pearsonr
import pandas as pd
import logging
from eventcontext import context
from pandas import tseries
from logging.handlers import RotatingFileHandler
from datetime import datetime

import os

class similarpurchasersbynearestneighbor:
    #first this class loads the products , customers data
    # Then it does a merge of the products,customers to provide a merged view
    # Then a pivot is created for all customers by product
    #Finally using pearsonr coefficient, for every user and product in his purchase, other purchasers basket or purchase is evaluated and
    #based on the similarity based on pearsonr coeff, the users are sorted and returned

    dfprod = pd.DataFrame()
    dforder = pd.DataFrame()
    dfcustprodmatrix = pd.DataFrame()

    logger = logging.getLogger("bespoke")
    logger.setLevel(logging.INFO)
    logger.handlers.append(RotatingFileHandler("recommender.log","a",50000000,2))

    def __init__(self):
        self.logger.info("Time started is {}".format(datetime.now().strftime("%d-%m-%Y %H:%M:%S")))
        prodfile = os.path.join(os.path.dirname(__file__),"stub/products.csv")
        orderfile = os.path.join(os.path.dirname(__file__),"stub/customerorder.csv")
        self.dfprod = pd.read_csv(prodfile,header=0, encoding='ISO-8859-1' ,dtype={"productid":"int"}) #names=["productid","categoryid","categoryname","brand"])#names=["brand","categoryid","categoryname","color","productid"])
        self.dforder = pd.read_csv(orderfile,header=0,encoding='ISO-8859-1',dtype={"customerid":"int","productid":"int"} )#names=["customerid","productid","ordereddate"])
        self._createcustomerorderpivot()
        self.logger.info("Init completed, loading the products & customers")

    def _createcustomerorderpivot(self):
        #for now will have inner join
        self.dfmergedprodcust = pd.merge(self.dfprod,self.dforder,how="inner",on="productid")
        logging.info("Customerprod generated successfully")
        self.dfcustprodmatrix = pd.pivot_table(self.dfmergedprodcust,index="customerid",columns="productid",values="qty")
        print(self.dfcustprodmatrix.head())
        self.logger.info("userproduct pivot created and has {} rows".format(len(self.dfcustprodmatrix)))

        dfcust = self.dforder["customerid"].unique()


    def _similaritybeweenusers(self,user1,user2):
        '''Mean is not required as the way we have built logic is 0 or 1 i.e binary representation against product'''
        user11 = np.array(user1) - np.mean(user1)
        user22 = np.array(user2) - np.mean(user2)
        '''find products which both have purchased'''
        commonbought=[]
        notbought = []

        for prod in range(len(user11)):
            if user11[prod] > 0 or user22[prod] > 0:
                commonbought.append(prod)
        if len(commonbought) == 0:
            return  0
        else:
            user1 =  np.array(np.nan_to_num([user11[i] for i in commonbought]))
            user2 = np.array(np.nan_to_num([user22[i] for i in commonbought]))
            print("Pearsoncoeff is {}".format(pearsonr(user1,user2)))
            print("numpy coeff is {}".format(np.corrcoef(user1,user2)))
            return pearsonr(user1,user2)[0]

    def getnearestneighbours(self,activeuser,K):
        #Call the method by passing the user and the next "K" closest neighbors of the user
        #This logic uses purchase history to find nearest users
        #This method should not be used for service. As of now optimized for batch operations only
        #WIll refine before providing the service for front end

        similaritymatrix = pd.DataFrame()
        similaritymatrix = pd.DataFrame(index = self.dfcustprodmatrix.index, columns=['similarity'])
        activeuser = float(activeuser)

        #lists all the users with empty similarity dataframe.
        for index in self.dfcustprodmatrix.index:
            #We need to skip where index value is same as user
            index = int(index)
            if index != activeuser:

                #get similarity score
                # finds similarity b/w activeuser and user in customer matrix index. This will iterate similarity
                # the activeuser and all other users.
                simlarityscore = self._similaritybeweenusers(self.dfcustprodmatrix.loc[activeuser],
                                                                      self.dfcustprodmatrix.loc[index])
                self.logger.info("Similarity score for {} and {} is {}".format(activeuser,index,simlarityscore))
                similaritymatrix.loc[index] = simlarityscore

        similaritymatrix = pd.DataFrame.sort_values(similaritymatrix,['similarity'],ascending=[0])
        #now we get the top K users who are closest to the activeusers.
        nearestneighbors = similaritymatrix.head(K)

        self.logger.info("Nearest neighbors for {} completed at {}".format(activeuser, datetime.now().strftime("%d-%m-%Y %H:%M:%S")))

        return nearestneighbors
        '''Will improve the logic using gradient descent next'''


if __name__ == "__main__":
    rec = similarpurchasersbynearestneighbor()
    #Few users who got high number of purchases are :
    #10017
    print(rec.getnearestneighbours("10017",10))
