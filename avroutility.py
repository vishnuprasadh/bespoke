from avro import schema
import os
import logging
from logging.handlers import RotatingFileHandler
from configuration import configuration
from configuration import domainschema

class avroutility:

    config = configuration()
    logger = logging.getLogger("bespoke")
    handler = RotatingFileHandler("bespoke.log", mode="a", maxBytes=500000, backupCount=5)

    '''
    Pass the type of domain you would like to load
    '''
    def loadschema(self, domain):
        if not self.logger.handlers:
            self.logger.addHandler(self.handler)

        self.logger.setLevel(self.config.loglevel)
        self.logger.info("Started loadschema call for domain - {}".format(domain))
        if not type(domain) == domainschema:
            raise ValueError("Invalid domain schema sent, use domainschema Enum from the module to set this.")
        parsedoutput = ""
        try:
            schemaname=""
            schemastring = ""
            if domain.value == domainschema.PRODUCT.value:
                schemaname = self.config.productschemaname
            elif domain.value == domainschema.CUSTOMER.value:
                schemaname =  self.config.customerschemaname
            elif domain.value == domainschema.ORDER.value:
                schemaname = self.config.orderschemaname

            schemafile =  os.path.join(os.path.dirname(__file__), schemaname)

            self.logger.info("Schema {} to load from {}".format(schemaname, schemafile))

            with open(schemafile,'r') as f:
                '''key is to parse and check if its valid'''
                parsedoutput = schema.Parse(f.read())
                f.close()
                self.logger.info("Schema load complete")
        except Exception as ex:
            self.logger.exception(ex)
        finally:
            self.logger.info("Completed loadschema call for domain - {}".format(domain))
            return parsedoutput


#test code
if __name__ == "__main__":
    domain = domainschema.ORDER | domainschema.PRODUCT
    avr = avroutility()
    #print(avr.loadschema(domainschema.CUSTOMER))
    #print(avr.loadschema(domainschema.PRODUCT))
    print(avr.loadschema(domainschema.ORDER))
