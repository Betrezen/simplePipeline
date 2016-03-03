# -*- python -*-
# author: krozin@gmail.com
# pylib: created 2016/02/01.
# copyright

import sys
import traceback
from threading import Thread

import pkg_resources

from log import logger


class CoreError(Exception):
    pass

class EOS(Exception):
    pass

class ProfiledThread(Thread):
    # Overrides threading.Thread.run()
    def run(self):
        import cProfile
        profiler = cProfile.Profile()
        try:
            return profiler.runcall(Thread.run, self)
        finally:
            profiler.dump_stats('myprofile-%d.profile' % (self.ident,))


class ThreadLoop(Thread):
    """ Simple Thread with loop implementation.
        Allows to stop the loop easily.
    """

    def __init__(self, *agrs, **kwargs):
        self.loop = kwargs.pop('loop')
        kwargs['target'] = self.myrun
        super(ThreadLoop, self).__init__(*agrs, **kwargs)
        self.running = True

    def myrun(self):
        while self.running:
            try:
                self.loop()
            except Exception as e:
                exc_type, exc_value, exc_tb = sys.exc_info()
                logger.error(''.join(traceback.format_exception(exc_type, exc_value, exc_tb)))
                return

    def stop(self):
        self.running = False
        self.join()


class PipelineModule(object):

    def __init__(self, pipe, name, config):
        super(PipelineModule, self).__init__()
        self.pipe = pipe
        self.name = name
        self.config = config
        self.module_init()
        self.enabled = True

    def module_init(self):
        pass

    def on_capabilities(self, caps):
        logger.info("on_capabilities")

    """ Start pipeline module. Start processing"""
    def start(self):
        logger.info("start")

    """ Stop pipeline module. Stop processing"""
    def stop(self):
        logger.info("stop")

    """ Process pipeline input. """
    def process(self, data):
        raise NotImplementedError('process method should be implemented')

    @property
    def conf(self):
        return self.conf

    """ enabling pipeline module """
    def enable(self):
        self.enabled = True

    """ disabling pipeline module """
    def disable(self):
        self.enabled = False

    def __repr__(self):
        return '<{self.__class__.__name__} name=\'{self.name}\', enabled={self.enabled}>'.format(self=self)


class Pipeline(list):

    modules = {}
    _loaded_modules = False

    @classmethod
    def register(cls, name):
        """ Decorator to register pipeline modules
        """
        def decorator(module_cls):
            cls.register_module(name, module_cls)
            return module_cls
        return decorator

    @classmethod
    def register_module(cls, name, module_cls):
        #if issubclass(module_cls, PipelineModule):
            cls.modules[name] = module_cls
            print ("register_module = {}".format(name))
        #else:
        #    raise CoreError('modules should be subclass of PipelineModule')

    @classmethod
    def load_modules(cls):
        if cls._loaded_modules:
            return
        # Load modules
        for plugin in pkg_resources.iter_entry_points('simplepipeline.modules'):
            try:
                mcls = plugin.load()
                print ("load_modules = {}".format(plugin.name))
            except Exception as e:
                print ('Unable to load plugin "{}" - {}'.format(plugin.name, e))
                continue

            print ("pa:{}".format(mcls.__subclasses__()))
            #if not issubclass(mcls, PipelineModule):
            #    print ('plugin "{}" is not a subclass of PipelineModule.'.format(plugin.name))
            #    continue
            cls.register_module(plugin.name, mcls)
        cls._loaded_modules = True

    def __init__(self, modules=None, config=None):
        list.__init__(self)
        self.config = config
        self.load_modules()

    def create_module(self, name):
        print self.modules
        print self.config.get(name, {})
        return self.modules.get(name)(self, name, self.config.get(name, {}))

    def get_module_by_name(self, name):
        for m in self:
            if m.name == name:
                return m

    def method_as_module(self, fn):
        module_cls = type('MethodModule', (PipelineModule, ), {'process': staticmethod(fn)})
        return module_cls(self, fn.__name__, self.config.get('', {}))

    def on_capabilities(self, caps):
        map(lambda a: a.on_capabilities(caps), self)

    def start(self):
        map(lambda a: a.start(), self)

    def stop(self):
        map(lambda a: a.stop(), self)

    def processing_loop(self):
        data = {}
        for module in self:
            if module.enabled:
                data = module.process(data)
        print data