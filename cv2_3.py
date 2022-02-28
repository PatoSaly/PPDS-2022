"""Fibonacci numbers
"""

from fei.ppds import Thread, Mutex, Semaphore, print, Event
from time import sleep
from random import randint


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
        self.M.lock()
        self.C += 1
        if self.C == self.N:
            self.C = 0
            # Different implementations for Semaphore and Event
            if isinstance(self.T, Event):
                self.T.signal()
            else:
                self.T.signal(self.N)
        print(self.C)
        self.M.unlock()
        self.T.wait()
        if isinstance(self.T, Event):
            self.clear()

    def clear(self):
        self.T.clear()


def compute_fibonacci(barrier1, barrier2, i):
    sleep(randint(1, 5)/10)
    fib_seq[i+2] = fib_seq[i] + fib_seq[i+1]


THREADS = 10

fib_seq = [0] * (THREADS + 2)
fib_seq[1] = 1

barrier1 = SimpleBarrier(THREADS)
barrier2 = SimpleBarrier(THREADS)

threads = [Thread(compute_fibonacci, barrier1, barrier2, i)
           for i in range(THREADS)]

for i in range(THREADS):
    compute_fibonacci(barrier1, barrier2, i)

print(fib_seq)

[t.join() for t in threads]

print(fib_seq)
