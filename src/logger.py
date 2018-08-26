import time

class logit(object):
    def __init__(self, logfile='../logs/out.log'):
        self.logfile = logfile

    def __call__(self, func):
        log_string = time.time() + ' : ' + func.__name__  
        with open(self.logfile, 'a') as f:
            f.write(log_string + '\n')
        
