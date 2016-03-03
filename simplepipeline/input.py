# -*- python -*-
# author: krozin@gmail.com
# pylib: created 2016/02/01.
# copyright

import Queue
import time
import os
from os.path import join, getsize

from pipeline import PipelineModule
from log import logger
import pylib

class DummyInput(PipelineModule):
    """ dummy """
    def module_init(self):
        super(DummyInput, self).module_init()
        self.queue = Queue.Queue(maxsize=60)
        self.capabilities_posted = False
        self._craete_pipeline()

    def _craete_pipeline(self):
        logger.info("_craete_pipeline")

    def start(self):
        super(DummyInput, self).start()
        logger.info("DummyInput start")

    def stop(self):
        super(DummyInput, self).stop()
        logger.info("DummyInput stop")

    def run(self):
        for directory in self.config.get('target_dir'):
            files = pylib.check_new_files(directory)
            for f in files:
                with open(f, 'r') as content_file:
                    content = content_file.read()
                try:
                    self.queue.put_nowait(content)
                except Queue.Full:
                    self.queue.empty()
                    pass
                os.remove(f)
        return True

    def process(self, data):
        fileins = []
        if self.queue.qsize() == 0:
            while True:
                # get files and put it to queue
                self.run()
                try:
                    fileins.append(self.queue.get(timeout=1))
                except Queue.Empty:
                    print ("nothing to handle")
                else:
                    break
        else:
            try:
                while True:
                    fileins.append(self.queue.get_nowait())
            except Queue.Full:
                self.queue.clear()
                pass
            except Queue.Empty:
                pass

        for i in fileins:
            data['filein'] = i
            data['filesize'] = len(i)
            data['in_timestamp'] = time.time()

        time.sleep(1)
        return data