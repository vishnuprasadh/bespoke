import pandas as pd
import os
import kafka


class productstub(object):
    def generate(self):
        filename = os.path.join( os.path.dirname(__file__), "sampleitem.csv")
        df = pd.read_csv(filename)

        if df:
            pass
        print(df.head())



class customerstub(object):
    pass

class orderstub(object):
    pass


prod = productstub()
prod.generate()