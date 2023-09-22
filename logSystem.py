import logging
import os

def create_logger(filepath:str) -> logging.Logger:
    '''create a new logger object'''

    if not os.path.exists(os.path.dirname(filepath)):
        return None
    logging.basicConfig(filename=filepath, level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', filemode="w")
    logger = logging.getLogger()
    return logger