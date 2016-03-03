# -*- python -*-
# author: krozin@gmail.com
# pylib: created 2016/02/01.
# copyright

import sys
import traceback
import datetime
import time
import threading

from log import logger
from pipeline import ThreadLoop
from pipeline import Pipeline, EOS

from yamlloader import attrdict, get_env

class App(object):

    exit_cond = threading.Event()

    def __init__(self, configfile):
        logger.info('App: starting ...')
        self.configfile = configfile
        self.config = get_env(self.configfile)
        self.pipe = Pipeline(config=self.config)

        # let's do init according to our purpose: IN next OUT
        self.finput = self.pipe.create_module('file_input')
        self.pipe.append(self.finput)

        self.output = self.pipe.create_module('file_output')
        self.pipe.append(self.output)

        self.pipe.start()
        self.core_processor = ThreadLoop(loop=self.processing_queue_loop)
        self.core_processor.start()

    def main(self):
        rc = 0
        try:
            while not self.exit_cond.wait(.1):
                time.sleep(.1)
        except KeyboardInterrupt as e:
            logger.warn('App: KeyboardInterrupt')
            rc = -1
        self.on_exit()

        logger.info('App: exited with {}'.format(rc))
        return rc

    def processing_queue_loop(self):
        try:
            self.pipe.processing_loop()
        except EOS as e:
            logger.info('App: EOS')
            self.core_processor.running = False
            self.quit()
        except Exception as e:
            exc_type, exc_value, exc_tb = sys.exc_info()
            logger.error('App: Fatal exception in processing_queue_loop')
            logger.error('App: ' + ''.join(traceback.format_exception(exc_type, exc_value, exc_tb)))
            self.core_processor.running = False
            self.quit()

    def quit(self):
         self.exit_cond.set()

    def on_exit(self):
        logger.info('App: exit')
        self.pipe.stop()
        self.core_processor.stop()
