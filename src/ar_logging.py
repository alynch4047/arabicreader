

import logging

from server import configuration

root_logger = logging.getLogger()
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')

initialised = False
def initialise():
    global initialised
    if not initialised:
        # tail -F /tmp/arlogging.log to see debugging
        hdlr = logging.FileHandler(configuration.log_file)
        hdlr.setFormatter(formatter)
        root_logger.addHandler(hdlr)
        root_logger.level = logging.DEBUG
        
    initialised = True
    
initialise()
    
hdlr = None    
    
std_out_added = False
def add_std_out():
    global hdlr, std_out_added
    if std_out_added:
        return
    std_out_added = True
    hdlr = logging.StreamHandler()
    hdlr.setFormatter(formatter)
    root_logger.addHandler(hdlr)
    
def remove_std_out():
    global hdlr
    root_logger.removeHandler(hdlr)
    
