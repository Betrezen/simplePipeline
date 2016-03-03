# -*- python -*-
# author: krozin@gmail.com
# pylib: created 2016/02/01.
# copyright


from setuptools import setup, Extension, find_packages
from Cython.Distutils import build_ext


setup(
    name='simplepipeline',
    version="1.0",
    packages=find_packages(),
    install_requires=['cython',],
    #cmdclass={'build_ext': build_ext},
    entry_points={
       'simplepipeline.modules': [
           # Input / Output
           'file_input = simplepipeline.input:DummyInput',
           'file_output = simplepipeline.output:DummyOutput',

           # Processing
           #'csv_processor = simplepipeline.processing:CSVextractor',
           #'sql_processor = simplepipeline.processing:SQLextractor',
           #'json_processor = simplepipeline.processing:JSONextractor',

           # Debug
           #'debug = simplepipeline.debug:Debugger',
           #'logger = simplepipeline.debug:Logger',
       ]
    },
    #scripts=['tools/generator.py',]
)
