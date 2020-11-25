import logging

class ConfigureLogs():
    def configure_log(self,fname):
        logging.basicConfig(filename=fname+"_logs.log", 
                    format='%(asctime)s %(message)s', 
                    filemode='a')
        log_obj = logging.getLogger()
        log_obj.setLevel(logging.DEBUG)
        return log_obj