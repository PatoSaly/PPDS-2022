import time

from fei.ppds import Semaphore, Mutex, print, Thread
from random import randint
from time import sleep
from matplotlib import pyplot as plt


class Shared:
    def __init__(self, n):
        self.finished = False
        self.mutex = Mutex()
        self.free = Semaphore(n)
        self.items = Semaphore(0)


def producer(shared):
    while True:
        # production
        sleep(randint(1, 10)/10)
        shared.free.wait()
        if shared.finished:
            break
        shared.mutex.lock()
        # store product in warehouse
        sleep(randint(1, 10)/100)

        shared.mutex.unlock()
        shared.items.signal()


def consumer(shared):
    while True:
        shared.items.wait()
        if shared.finished:
            break
        shared.mutex.lock()
        # get product from Warehouse
        sleep(randint(1, 10)/100)
        shared.mutex.unlock()
        # consume product
        sleep(randint(1, 10)/10)


def main():
    for i in range(10):
        time1 = time.perf_counter()
        s = Shared(10)
        c = [Thread(consumer, s) for _ in range(2)]
        p = [Thread(producer, s) for _ in range(5)]

        sleep(3)
        s.finished = True

        time2 = time.perf_counter()
        print(f"Hlavne vlakno: caka na dokoncenie")
        s.items.signal(100)
        s.free.signal(100)
        [t.join() for t in c+p]
        print(f"Hlavne vlakno: koniec programu")
        print(f"cas trvania: {time2 - time1:0.4f} sekund")


if __name__ == "__main__":
    main()
