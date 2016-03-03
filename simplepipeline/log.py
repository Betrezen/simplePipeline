# -*- python -*-
# author: krozin@gmail.com
# pylib: created 2016/02/01.
# copyright


import logging


class MyFormatter(logging.Formatter):

    def format(self, record):
        try:
            msg = record.msg.split(':', 1)
            if len(msg) == 2:
                record.msg = '[{:<15}]{}'.format(msg[0], msg[1])
        except:
            pass
        return logging.Formatter.format(self, record)


logger = logging.getLogger('pipeline')
logger.setLevel(logging.DEBUG)

f = '[%(asctime)s][%(processName)-5s][%(levelname)-21s]%(message)s'
formatter = MyFormatter(f)
fileformatter = logging.Formatter(f)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# Log level colors
logging.addLevelName(logging.DEBUG, "\033[1;34m{}\033[1;0m".format(logging.getLevelName(logging.DEBUG)))
logging.addLevelName(logging.INFO, "\033[1;32m{}\033[1;0m".format(logging.getLevelName(logging.INFO)))
logging.addLevelName(logging.WARNING, "\033[1;33m{}\033[1;0m".format(logging.getLevelName(logging.WARNING)))
logging.addLevelName(logging.ERROR, "\033[1;31m{}\033[1;0m".format(logging.getLevelName(logging.ERROR)))
logging.addLevelName(logging.CRITICAL, "\033[1;41m{}\033[1;0m".format(logging.getLevelName(logging.CRITICAL)))


def add_file_handler(fname):
    file_handler = logging.FileHandler(fname)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(fileformatter)
    logger.addHandler(file_handler)
