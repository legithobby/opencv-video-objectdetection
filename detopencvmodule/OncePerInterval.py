import time as opitime
from threading import Thread, Lock
import os

class OncePerInt:
    def __init__(self, callbackfu):
        #self.delaysec = delay
        #self.prevtime = time.time() - delay
        self.cb_func = callbackfu
        self.lock = Lock()  # Create a lock

    def setcb(self, func):
        self.cb_func = func

    def task(self):
        if self.lock.locked():
            print("Locked, return without starting new task")
            return
        with self.lock:
            self.cb_func()
        
    def runcmd(self, *args, **kwargs):
        t1 = Thread(target=self.task)
        t1.start()

