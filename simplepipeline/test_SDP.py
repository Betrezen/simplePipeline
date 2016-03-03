# -*- python -*-
# author: krozin@gmail.com
# pylib: created 2016/02/01.
# copyright


import unittest
from yamlloader import attrdict, get_env
from app import App

class TestSimplePipeline(unittest.TestCase):

    def setUp(self):
        self.configfile = './server.conf'
        self.config = get_env(self.configfile)

    def test_yaml(self):
        try:
            self.assertEqual(isinstance(self.config, attrdict), True)
            print (self.config.viewitems())
            print (self.config.order)
            print (self.config.input)
        except Exception as e:
            print e

    #@unittest.skip
    def test_app(self):
        import pylib
        pylib.generate_tmp_files(self.config.get("file_input",{}).get("target_dir")[0])
        app = App("server.conf")
        app.main()

if __name__ == '__main__':
    unittest.main()