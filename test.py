from avro import schema as sc
from avro import datafile as df
from avro import io as avio


import os
from urllib import request
from urllib import response
from urllib import error
from io import  BytesIO
from kafka import KafkaProducer
from kafka.future import Future

try:

    channel = KafkaProducer(bootstrap_servers='localhost:9092', client_id="1", api_version= (0,10),request_timeout_ms=5000,acks=0 )
    msg = "Hello world!"
    future = channel.send(topic="test",value=msg.encode("utf-8"))
    meta = future.get(timeout=100)
    print(meta)
    if not meta:
        print(meta.topic)
except Exception as ex:
    print(ex)







'''

_prodschema = 'product.avsc'

dirname =  os.path.dirname(__file__)

avroschemaname = os.path.join( os.path.dirname(__file__),_prodschema)
sch = {}

with open(avroschemaname,'r') as f:
    sch= f.read().encode(encoding='utf-8')
    f.close()


proschema = sc.Parse(sch)

print("Schema processed")

writer =  df.DataFileWriter(open(os.path.join(dirname,"products.json"),'wb'),
                             avio.DatumWriter(),proschema)
print("Just about to append the json")
writer.flush()



writer.append ({ "id":"2334",
                "title": "Cool Footwears from Relaxo",
                "brand":"Relaxo",
                "description":"Cool footwears from relaxo are comfortable and are exceedingly great for comfort, available in S, L,XL,M sizes.",
                "keywords": ["relaxo", "shoe"],
                "unit":"Each",
                "price": 799.99,
                "url":"",
                "imageurl":"",
                "currency":"INR"
                })
writer.close()
'''