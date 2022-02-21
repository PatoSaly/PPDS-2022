from fei.ppds import Thread, Mutex
from collections import Counter
from time import sleep
from random import randint

class Shared:
    def __init__(self, size):
        self.counter = 0
        self.end = size
        self.elms = [0] * size


def do_count(shared):
    mutex.lock()
    while True:
        if shared.counter >= shared.end:
            break

        shared.elms[shared.counter] += 1
        sleep(randint(1, 10)/1000)
        shared.counter += 1

    mutex.unlock()

shared = Shared(1000)
mutex = Mutex()

t1 = Thread(do_count, shared)
t2 = Thread(do_count, shared)

t1.join()
t2.join()

counter = Counter(shared.elms)
print(counter.most_common())
