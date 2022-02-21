from fei.ppds import Thread, Mutex
from collections import Counter
from time import sleep
from random import randint


class Shared:
    """
    Instance of this class is shared between multiple threads
    """
    def __init__(self, size):
        """
        Constructor of class has one parameter -- size

        Object of class has 3 elements:
        counter -- index through array
        end -- size of array => parameter of Constructor
        elms -- array itself, each element initialized to 0
        """
        self.counter = 0
        self.end = size
        self.elms = [0] * size


def do_count(shared):
    """
    Function that increases each element by 1
    """
    while True:
        mutex.lock()
        #condition to end while loop when iterator (counter) is at the end of the array
        if shared.counter >= shared.end:
            mutex.unlock()
            break

        shared.elms[shared.counter] += 1
        #intentional error that puts a thread to sleep for a random time to achieve program execution inconsistency
        sleep(randint(1, 10)/1_000)
        shared.counter += 1

        mutex.unlock()


shared_object = Shared(1_000)
mutex = Mutex()

t1 = Thread(do_count, shared_object)
t2 = Thread(do_count, shared_object)

t1.join()
t2.join()

counter = Counter(shared_object.elms)
print(counter.most_common())