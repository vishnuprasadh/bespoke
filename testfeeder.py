import pandas as pd
import numpy as np
import os
from json import dumps
import json
from kafkautility import kafkafactory

class testfeeder:

    def loadproducts(self):
        try:
            chunk = pd.DataFrame()
            kf = kafkafactory()
            df = pd.read_csv(os.path.join(os.path.dirname(__file__),"stub/sampleitem.csv"),chunksize=2)
            for chunk in df:
                data = ""
                data = chunk.to_json(orient="records")
                jdata = json.loads(data)
                kf.sendmessage(kafkafactory.MessageType.Test,jdata)
        except Exception as ex:
            print(ex)


test = testfeeder()
test.loadproducts()