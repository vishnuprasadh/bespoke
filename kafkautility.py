from kafka import KafkaProducer
from kafka import KafkaConsumer
from kafka import BrokerConnection
from kafka.errors import KafkaError
from kafka.future import Future
from json import dumps
import json
import kafka
import os
import logging
from logging.handlers import RotatingFileHandler
from configparser import ConfigParser
from enum import Enum,IntFlag,unique
import time
import datetime
from kafka.common import TopicPartition



class kafkafactory:
    @unique
    class MessageType(IntFlag):
        Product = 1,
        Customer = 3,
        Order = 5,
        Rating = 7,
        Promotion = 9,
        Category = 11,
        Test = 15




    logger = logging.getLogger("bespoke")
    logger.setLevel(logging.ERROR)
    handler = RotatingFileHandler("bespoke.log", mode="a", maxBytes=500000, backupCount=5)

    _producttopic =""
    _customertopic =""
    _promotopic=""
    _ratingtopic = ""
    _ordertopic = ""
    _categorytopic=""
    _testtopic=""

    _productsource =""
    _customersource= ""
    _ordersource=""
    _categorysource =""
    _promotionsource =""
    _ratingsource =""

    _version = ""

    '''Producer config values'''
    _broker_list=""
    _request_required_acks= 0
    _producer_type=""
    _client_id =""
    _message_send_max_retries = 0
    _request_timeout_ms = 0
    _batch_size= 0
    _compression_codec=""

    '''Broker config value'''
    _zookeeper_connect =""


    def __init__(self):
        try:
            defaultsection = "kafkaconfig"
            brokersection = "brokerconfig"
            producersection = "producerconfig"
            consumersection ="consumerconfig"

            if not self.logger.handlers:
                self.logger.addHandler(self.handler)
            config = ConfigParser()
            config.read( os.path.join(os.path.dirname(__file__),"bespoke-kafka.cfg"))
            self.logger.setLevel(config.get(section=defaultsection,option="loglevel"))

            self.logger.info("Started init of kafka utility")

            self._producttopic = config.get(section=defaultsection,option="producttopic")
            self._customertopic= config.get(section=defaultsection,option="customertopic")
            self._promotopic= config.get(section=defaultsection,option="promotopic")
            self._ratingtopic= config.get(section=defaultsection,option="ratingtopic")
            self._categorytopic = config.get(section=defaultsection, option="categorytopic")
            self._ordertopic= config.get(section=defaultsection,option="ordertopic")
            self._productsource= config.get(section=defaultsection,option="productsource")
            self._customersource = config.get(section=defaultsection, option="customersource")
            self._ordersource = config.get(section=defaultsection, option="ordersource")
            self._categorysource = config.get(section=defaultsection, option="categorysource")
            self._promotionsource = config.get(section=defaultsection, option="promotionsource")
            self._ratingsource = config.get(section=defaultsection, option="ratingsource")
            self._testtopic = config.get(section=defaultsection, option="testtopic")
            self._version = config.get(section=defaultsection, option="version")

            '''A bad technique required to ensure proper version is sent'''
            version = self._version.split(",")
            version = [int(x) for x in sorted(version)]
            self._version = tuple(version)


            '''load the zookeeper config '''
            self._zookeeper_connect = config.get(section=brokersection, option="zookeeper.connect")

            '''load all producer config'''
            self._broker_list = config.get(section=producersection, option="broker.list")
            self._request_required_acks = int(config.get(section=producersection, option="request.required.acks"))
            self._request_timeout_ms = int(config.get(section=producersection, option="request.timeout.ms"))
            self._producer_type = config.get(section=producersection, option="producer.type")
            self._client_id = config.get(section=producersection, option="client.id")
            self._message_send_max_retries = int( config.get(section=producersection, option="message.send.max.retries"))
            self._batch_size = int( config.get(section=producersection, option="batch.size"))
            self._compression_codec = config.get(section=producersection, option="compression.codec")

            print(self._ordersource)
        except Exception as ex:
            self.logger.error(ex)
        finally:
            self.logger.info("Completed init of kafka utility")

    def sendmessage(self, messagetype,message):
        metadata =""
        try:
            connectiondetails = self._resovlesendmessagetype (messagetype)
            client = connectiondetails[0]
            topic = connectiondetails[1]

            localtime = time.localtime()
            epochtime = time.mktime(localtime)
            message = str(message).encode()
            future = client.send(topic=topic, value=message)
            metadata = future.get(timeout=3)
        except KafkaError as Kerr:
            self.logger.exception("Kafka error occurred! - {}".format(Kerr))
        except Exception as ex:
            self.logger.exception(ex)
        finally:
            self.logger.info("Exiting send message successfully")
            return metadata

    def readmessage(self,messagetype,consumergroup=None):
        message = ""
        try:
            connectiondetails = self._resolvegetmessage(messagetype)
            client = connectiondetails[0]
            topic = connectiondetails[1]

            return client._resolvegetmessage(messagetype)

        except KafkaError as KError:
            self.logger.exception("Kafka error occured! - {}".format(KError))
        except Exception as err:
            self.logger.exception(err)
        finally:
            return message


    def _resolvegetmessage(self, messagetype):
        messagedict = dict()


        topic= self._gettopicbasedonmessagetype(messagetype)

        consumer = KafkaConsumer(topic,
                               bootstrap_servers=self._broker_list,
                               api_version=tuple(self._version),
                               client_id=self._client_id,
                               request_timeout_ms = self._request_timeout_ms,
                               max_partition_fetch_bytes=1000,
                               auto_commit_interval_ms = 4000,
                               auto_offset_reset='earliest',
                               enable_auto_commit=False,
                               )
        for msg in consumer:
            value = msg.value.decode()
            timestamp = msg.timestamp
            offset = msg.offset
            messagedict[offset] = value
            print(value)
            consumer.commit()
        return messagedict


    '''Resolves the Kafka SimpleClient internally based on messagetype passed. The second param also returns the topic name'''
    def _resovlesendmessagetype(self,messagetype):
        client = KafkaProducer(bootstrap_servers=self._broker_list, api_version= tuple(self._version),
                               client_id=self._client_id,
                               request_timeout_ms=self._request_timeout_ms,
                               acks=self._request_required_acks,
                               retries=self._message_send_max_retries)

        topic = self._gettopicbasedonmessagetype(messagetype)

        return [client, topic]

    def _gettopicbasedonmessagetype(self,messagetype):
        if messagetype == self.MessageType.Test:
            topic = self._testtopic
        elif messagetype == self.MessageType.Product:
            topic = self._producttopic
        elif messagetype == self.MessageType.Customer:
            topic = self._customertopic
        elif messagetype == self.MessageType.Order:
            topic = self._ordertopic
        elif messagetype == self.MessageType.Category:
            topic = self._categorytopic
        elif messagetype == self.MessageType.Rating:
            topic = self._ratingtopic
        elif messagetype == self.MessageType.Promotion:
            topic = self._promotopic
        return topic



if __name__ == "__main__":
    k = kafkafactory()
    #for i in range(1,2):
    #    print(k.sendmessage(kafkafactory.MessageType.Test,"Hello Product!!!! {}".format(i)))
    k.readmessage(kafkafactory.MessageType.Test)
