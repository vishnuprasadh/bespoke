import numpy as np
import scipy as sc
import pandas as pd
from eventcontext import context
import os
from pandas import tseries

class recommender:
    dfprod = pd.DataFrame()
    dforder = pd.DataFrame()

    def __init__(self):

        #df = pd.read_csv("av",)
        prodfile = os.path.join(os.path.dirname(__file__),"stub/products.csv")
        orderfile = os.path.join(os.path.dirname(__file__),"stub/customerorder.csv")
        #pd.read_csv(prodfile,header=0,)
        dfprod = pd.read_csv(prodfile,header=0, encoding='ISO-8859-1') #names=["productid","categoryid","categoryname","brand"])#names=["brand","categoryid","categoryname","color","productid"])
        dforder = pd.read_csv(orderfile,header=0,encoding='ISO-8859-1')#names=["customerid","productid","ordereddate"])
        dfprod.reset_index()#("productid",append=True)
        dforder.reset_index()#("productid",append=True)
        print(dfprod.head())
        print(dforder.head())
        self.dfprodorder = pd.merge(self.dfprod, self.dforder, how="outer",on="productid")


    def getproductsforuser(self,userid,ctxt=None):
        dfprodorder = pd.DataFrame()

        if ctxt == None:
            ctxt = context(1)

        #self.dfprodorder = pd.merge(self.dfprod, self.dforder,how="outer",left_on="productid",right_on="productid")
        #print(self.dfprodorder.head())

rec = recommender()
ctx = context(1,productid=3000303)
rec.getproductsforuser('10000')

pd.pivot_table()