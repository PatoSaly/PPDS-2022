from time import sleep
from random import randint
from fei.ppds import Thread, Mutex, Semaphore, print
 

class SimpleBarrier:
    def __init__(self, N):
        self.N = N
        self.C = 0
        self.M = Mutex()
        self.T = Semaphore(0)
 
    def wait(self):
        self.M.lock()
        self.C += 1
        if self.C == self.N:
            self.C = 0
            self.T.signal(self.N)
        self.M.unlock()
        self.T.wait()

 
def rendezvous(thread_name):
    sleep(randint(1,10)/10)
    print('rendezvous: %s' % thread_name)
 
 
def ko(thread_name):
    sleep(randint(1,10)/10)
    print('ko: %s' % thread_name)
 
 
def barrier_example(barrier1, barrier2, thread_name):
    """Kazde vlakno vykonava kod funkcie 'barrier_example'.
    Doplnte synchronizaciu tak, aby sa vsetky vlakna pockali
    nielen pred vykonanim funkcie 'ko', ale aj
    *vzdy* pred zacatim vykonavania funkcie 'rendezvous'.
    """
 
    while True:
        rendezvous(thread_name)
        barrier1.wait()
        ko(thread_name)
        barrier2.wait()
        
 
b1 = SimpleBarrier(5)
b2 = SimpleBarrier(5)

threads = list()
for i in range(5):
    t = Thread(barrier_example, b1, b2, i)
    threads.append(t)
 
for t in threads:
    t.join()