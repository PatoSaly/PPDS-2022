"""Solution to the synchronisation problem of savages and cooks
"""

from time import sleep
from random import randint
from fei.ppds import Semaphore, Thread, print, Mutex

N = 5
M = 8
C = 10


class SimpleBarrier:
    """Simple Barrier implementation with special outputs for savages, cooks problem
    Parameters:
        N - number of Threads
        C - counter
        M - Mutex lock
        T - Semaphore lock
    Functions:
        init - initialization of variables
        wait() - waiting until all threads are on same instruction
            Parameters:
                each - string that is printed by every thread
                     - used just to debug, no synchronization usage
                     - default is empty
                last - string that is printed by last thread
                     - used just to debug, no synchronization usage
                     - default is empty
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
    """Shared object
    Init parameters:
        servings - count of servings
                 - defined with construction of shared object
        mutexS, mutexC - different mutex for savages and cooks
        empty_pot - Semaphore lock that let cooks know when pot is empty
        full_pot - Semaphore lock that let savages know when pot is full
        cooks_count - counter of cooks
                    - used to find out when all cooks finished cooking
        s1, s2, c1, c2 - two barriers for savages and cooks
    """
    def __init__(self, m):
        self.servings = m
        self.mutexS = Mutex()
        self.mutexC = Mutex()
        self.empty_pot = Semaphore(0)
        self.full_pot = Semaphore(0)

        self.cooks_count = 0

        self.s1 = SimpleBarrier(N)
        self.s2 = SimpleBarrier(N)

        self.c1 = SimpleBarrier(C)
        self.c2 = SimpleBarrier(C)


def eat(i):
    print(f"savage {i}: eating")
    sleep(randint(50, 200)/100)


def savage(i, shared):
    """Main function of savages
    Two barriers will provide that savages eats together
    Savage that find out that there is no serving in pot
    call signal on empty_pot Semaphore that will let cooks
    continue in their function
    """
    # random reorder savages
    sleep(randint(1, 100)/100)
    while True:
        shared.s1.wait()
        shared.s2.wait(each=f"savage {i}: before dinner",
                       last=f"savage {i}: all savages are there")
        shared.mutexS.lock()
        if shared.servings == 0:
            print(f"savage {i}: empty pot")
            shared.empty_pot.signal(C)
            shared.full_pot.wait()
        print(f"savage {i}: take from pot")
        shared.servings -= 1
        shared.mutexS.unlock()
        eat(i)


def cook(j, shared):
    """Main function of cooks
    Cooking starts when pot is emtpy (savages call signal on empty_pot)
    Two barriers will provide that cooks cook together
    Last cook that finish his work signa that pot is full
    """
    while True:
        shared.empty_pot.wait()

        shared.c1.wait()
        shared.c2.wait(each=f"cook {j} waiting",
                       last=f"all cooks going to cook")

        shared.mutexC.lock()
        shared.cooks_count += 1
        shared.mutexC.unlock()

        print(f"cook {j}: cooking")
        sleep(randint(50, 200)/100)

        if shared.cooks_count == C:
            shared.servings += M
            print(f"cook {j}: {M} servings -> pot")
            shared.full_pot.signal()
            shared.cooks_count = 0



def main():
    shared = Shared(0)
    savages = []
    cooks = []

    for i in range(N):
        savages.append(Thread(savage, i, shared))
    for j in range(C):
        cooks.append(Thread(cook, j, shared))

    for t in savages + cooks:
        t.join()


if __name__ == "__main__":
    main()
