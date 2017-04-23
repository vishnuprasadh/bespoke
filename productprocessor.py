from avro import schema as sc
from avro import datafile as df
from avro import io as avio
import os
import time
import datetime
import json
from avroutility import avroutility
import configuration
from configuration import domainschema
class productprocessor(object):
    _prodschema = 'product.avsc'

    def processdata(self,data):
        #loads the schema of product using avroutility.
        #TODO processing of the entire feed through KAFKA
        utility = avroutility()
        self._prodschema = utility.loadschema(domain=domainschema.PRODUCT)
        print(self._prodschema)

if __name__ == '__main__':
    pp = productprocessor()
    pp.processdata(None)