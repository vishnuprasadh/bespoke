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
        utility = avroutility()
        self._prodschema = utility.loadschema(domain=domainschema.PRODUCT)



        '''
        print("Schema processed")
        writer =  df.DataFileWriter(open(os.path.join(dirname,"products.json"),'wb'),
                                         avio.DatumWriter(),proschema)
        print("Just about to append the json")

        date = str(datetime.time())
        writer.append({ "id":"23232",
                        "title":"Blue denim jeans",
                        "description": "A blue rich denim jeans from the world of Kaya"
                        })



        reader = df.DataFileReader(open(os.path.join(dirname,"products.json"),'r'),avio.DatumReader(),proschema)

        for product in reader:
            print(product)
        reader.close()
        '''


if __name__ == '__main__':
    pp = productprocessor()
    pp.processdata(None)