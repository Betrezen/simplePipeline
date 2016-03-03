# -*- python -*-
# author: krozin@gmail.com
# pylib: created 2016/02/01.
# copyright

import Queue
from log import logger
import os
from pipeline import PipelineModule
import pylib


class DummyOutput(PipelineModule):
    """ Output """
    def module_init(self):
        self.fileout = None
        self.queue = Queue.Queue(maxsize=30)

    def on_capabilities(self, caps):
        self._craete_pipeline()
        self.start()

    def _craete_pipeline(self):
        logger.info("_craete_pipeline")

    def start(self):
        logger.info("start")
        pass

    def stop(self):
        logger.info("stop")
        pass

    def process(self, data):
        tdir = self.config.get('target_dir',[])[0]
        if not os.path.exists(tdir):
            os.makedirs(tdir)
        fname = os.path.join(tdir, pylib.generate_file_name())
        print fname
        with open(fname, 'w') as ff:
            ff.write(str(data))
        data['fileout'] = fname
        return data