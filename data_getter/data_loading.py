from logging_.log import logging
import pandas as pd
"""
CLASS DEFINED TO READ DATA USING PANDAS LIBRARY
"""
class datagetter:
    def __init__(self, data_loc):
        self.data_loc = data_loc
        self.log_file = 'logging_/data_info_log.txt'

    def readfile(self):
        self.logobj = logging(self.log_file, 'ENTERED TO DATA LOADING -> DATA GETTER MODULE')
        self.logobj.log()
        try:
            data = pd.read_excel(self.data_loc)
            self.logobj.appnd_log("DATA LOADED SUCCESSFULLY")
            return data
        except Exception as e:
            self.logobj.appnd_log("FAILED TO LOAD DATA EXCEPTION MESSAGE>>>>>> " + str(e))