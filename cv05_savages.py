from time import sleep
from random import randint
from fei.ppds import Semaphore, Thread, print, Mutex

N = 3
M = 20


class SimpleBarrier:
    """Simple Barrier implementation
    Parameters:
        N - number of Threads
        C - counter
        M - Mutex lock
        T - Semaphore lock
    Functions:
        init - initialization of variables
        wait() - waiting until all threads are on same instruction
    """
    def __init__(self, N):
        self.N = N
        self.C = 0
        self.M = Mutex()
        self.T = Semaphore(0)

    def wait(self, each="", last=""):
        # sleep(randint(1,10)/10)
        self.M.lock()
        self.C += 1
        if each != "":
            print(each)
        if self.C == self.N:
            if last != "":
                print(last)
            self.C = 0
            self.T.signal(self.N)
        self.M.unlock()
        self.T.wait()


class Shared:
    def __init__(self, m):
        self.servings = m
        self.mutex = Mutex()
        self.empty_pot = Semaphore(0)
        self.full_pot = Semaphore(0)

        self.b1 = SimpleBarrier(N)
        self.b2 = SimpleBarrier(N)


def eat(i):
    print(f"savage {i}: eating")
    sleep(randint(50, 200)/100)


def savage(i, shared):
    # random reorder savages
    sleep(randint(1, 100)/100)
    while True:
        shared.b1.wait()
        shared.b2.wait(each=f"savage {i}: before dinner",
                       last=f"savage {i}: all savages are there")
        shared.mutex.lock()
        if shared.servings == 0:
            print(f"savage {i}: empty pot")
            shared.empty_pot.signal()
            shared.full_pot.wait()
        print(f"savage {i}: take from pot")
        shared.servings -= 1
        shared.mutex.unlock()
        eat(i)


def cook(shared):
    while True:
        shared.empty_pot.wait()
        print("cook: cooking")
        sleep(randint(50, 200)/100)
        print(f"cook: {M} servings -> pot")
        shared.servings += M
        shared.full_pot.signal()


def main():
    shared = Shared(0)
    savages = []

    for i in range(N):
        savages.append(Thread(savage, i, shared))
    savages.append(Thread(cook, shared))

    for t in savages:
        t.join()


if __name__ == "__main__":
    main()
