from configparser import ConfigParser
from configparser import ParsingError
import os
import logging
from logging.handlers import RotatingFileHandler

'''
Loads the configuration section and sets the params from configuration file.
'''
from enum import Enum,unique,IntFlag
@unique
class domainschema(IntFlag):
    PRODUCT =1
    ORDER = 2
    CUSTOMER =4

namespace = 'bespoke.avro'
sectionname=""
config = {}
productschemaname = ""
orderschemaname = ""
customerschemaname = ""
logpath = ""

class configuration(object):
    logger = logging.getLogger("bespoke")

    def __init__(self, sectionname="baseconfig"):
        try:
            if not self.logger.handlers:
                handler = RotatingFileHandler("bespoke.log", mode="a", maxBytes=500000, backupCount=5)
                self.logger.addHandler(handler)
            self.logger.setLevel(logging.ERROR)
            self.logger.info("configuration init started")
            file = os.path.join(os.path.dirname(__file__), "bespoke.cfg")
            self.sectionname = sectionname
            config = ConfigParser()
            config.read(file)
            self.productschemaname = config.get(section=sectionname, option="product")
            self.orderschemaname = config.get(section=sectionname, option="order")
            self.customerschemaname = config.get(section=sectionname, option="customer")
            self.loglevel = config.get(section=sectionname, option="loglevel")
            self.logpath = config.get(sectionname,option="logpath")
        except Exception as ex:
            raise ParsingError(source="configuration load for bespoke failed",filename="bespoke.cfg")
            self.logger.exception(ex)
        finally:
            self.logger.info("configuration init complete")
