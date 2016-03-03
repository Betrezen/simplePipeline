# -*- python -*-
# author: krozin@gmail.com
# pylib: created 2014/03/01.
# copyright

def get_random_mac():
    import random
    return ':'.join(map(lambda x: "%02x" % x, [0x00,0x16,0x3e,random.randint(0x00, 0x7f),random.randint(0x00, 0xff),random.randint(0x00, 0xff)]))

def get_random_ip4():
    import random
    return ".".join(map(lambda x: str(random.randint(0,256)), [i for i in range(0,4)]))

def get_random_ip4net():
    import random
    return get_random_ip4()+"/"+str(random.choice([16,24]))

def get_random_uuid():
    import uuid
    import hashlib
    import os
    l = os.urandom(30).encode('base64')[:-1]
    return hashlib.sha256(l).hexdigest()

def generate_tmp_files(targetdict="/tmp/files/"):
    import os
    import random
    import time
    import threading

    if not os.path.exists(targetdict):
        os.makedirs(targetdict)
    class FileThread(threading.Thread):
        def run(self):
            print "run"
            while(True):
                filenames = []
                countf = (random.choice([1,2,3]))
                for i in xrange(0, countf):
                    filenames.append(os.path.join(targetdict, get_random_uuid()))
                for i in filenames:
                    with (open(i, 'w')) as nfile:
                        nfile.write(get_random_ip4())
                time.sleep(1)
    mythread = FileThread()
    mythread.start()

def generate_file_name():
    from datetime import datetime
    import random
    filename = "_".join([datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S"), str(random.randint(1,100))])
    return filename


def check_new_files(directory):
    import os
    new_files = []
    for root, _, files in os.walk(directory):
        if files:
            abs_root = os.path.abspath(root)
            for fd in files:
                new_files.append(os.path.join(abs_root, fd))
        break
    return new_files

# decorator which print how many time were spend on fucntion
def benchmark(func):
    import time
    def wrapper(*args, **kwargs):
        t = time.clock()
        res = func(*args, **kwargs)
        #print func.__name__
        print(time.clock() - t)
        return res
    return wrapper

# decorator which counting call of function
def counter(func):
    def wrapper(*args, **kwargs):
        wrapper.count += 1
        res = func(*args, **kwargs)
        print("{0} invoked: {1}x times".format(func.__name__, wrapper.count))
        return res
    wrapper.count = 0
    return wrapper

