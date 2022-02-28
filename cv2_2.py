from time import sleep
from random import randint
from fei.ppds import Thread, Mutex, Semaphore, print, Event


class SimpleBarrier:
    """Simple Barrier implementation
    Parameters:
        N - number of Threads
        C - counter
        M - Mutex lock
        T - Semaphore lock
          - Evetnt lock

    Functions:
        init - initialization of variables
        wait() - waiting until all threads are on same instruction
        clear() - help to wait function
    """
    def __init__(self, N):
        self.N = N
        self.C = 0
        self.M = Mutex()
        # self.T = Event()
        self.T = Semaphore(0)

    def wait(self):
        # sleep(randint(1,10)/10)
        self.M.lock()
        self.C += 1
        if self.C == self.N:
            self.C = 0
            # Different implementations for Semaphore and Event
            if isinstance(self.T, Event):
                self.T.signal()
            else:
                self.T.signal(self.N)
        self.M.unlock()
        self.T.wait()
        if isinstance(self.T, Event):
            self.clear()

    def clear(self):
        self.T.clear()


def rendezvous(thread_name):
    sleep(randint(1, 10)/10)
    print('rendezvous: %s' % thread_name)


def ko(thread_name):
    sleep(randint(1, 10)/10)
    print('ko: %s' % thread_name)


def barrier_example(barrier1, barrier2, thread_name):
    while True:
        rendezvous(thread_name)
        barrier1.wait()
        ko(thread_name)
        barrier2.wait()

# Two threads
b1 = SimpleBarrier(5)
b2 = SimpleBarrier(5)

threads = list()
for i in range(5):
    t = Thread(barrier_example, b1, b2, i)
    threads.append(t)

for t in threads:
    t.join()
