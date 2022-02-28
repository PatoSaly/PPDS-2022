from random import randint
from time import sleep
from fei.ppds import Thread, Semaphore, Mutex, print
 
 
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
 
 
def barrier_example(barrier, thread_id):
    sleep(randint(1,10)/10)
    print("vlakno %d pred barierou" % thread_id)
    barrier.wait()
    print("vlakno %d po bariere" % thread_id)
 
 
sb = SimpleBarrier(5)

threads = []
for i in range(5):
    t = Thread(barrier_example, sb, i)
    threads.append(t)

for t in threads:
    t.join()