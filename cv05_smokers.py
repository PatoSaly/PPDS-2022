"""Solution to the synchronisation problem of smokers
"""

from time import sleep
from random import randint
from fei.ppds import Semaphore, Thread, print, Mutex


class Shared:
    """Shared object
    """
    def __init__(self):
        self.tobacco = Semaphore(0)
        self.paper = Semaphore(0)
        self.match = Semaphore(0)

        self.isTobacco = 0
        self.isMatch = 0
        self.isPaper = 0

        self.pusherMatch = Semaphore(0)
        self.pusherTobacco = Semaphore(0)
        self.pusherPaper = Semaphore(0)

        self.mutexS = Mutex()

        self.agentSem = Semaphore(1)


def make_cigarette(name):
    print(f"{name} make cigarette\n")
    sleep(randint(1, 10) / 100)


def smoke(name):
    # print(f"smoker {name} smoke\n")
    sleep(randint(1, 10) / 100)


def smoker_match(shared):
    """Smoker with infinite amount of matches
    """
    while True:
        sleep(randint(1, 10) / 100)
        shared.pusherMatch.wait()
        make_cigarette("match")
        shared.agentSem.signal()
        smoke("match")


def smoker_tobacco(shared):
    """Smoker with infinite amount of tobacco
    """
    while True:
        sleep(randint(1, 10) / 100)
        shared.pusherTobacco.wait()
        make_cigarette("tobacco")
        shared.agentSem.signal()
        smoke("tobacco")


def smoker_paper(shared):
    """Smoker with infinite amount of paper
    """
    while True:
        sleep(randint(1, 10) / 100)
        shared.pusherPaper.wait()
        make_cigarette("paper")
        shared.agentSem.signal()
        smoke("paper")


def agent_1(shared):
    while True:
        sleep(randint(1, 10) / 100)
        # shared.agentSem.wait()
        print("agent: tobacco, paper")
        shared.tobacco.signal()
        shared.paper.signal()


def agent_2(shared):
    while True:
        sleep(randint(1, 10) / 100)
        # shared.agentSem.wait()
        print("agent: match, paper")
        shared.match.signal()
        shared.paper.signal()


def agent_3(shared):
    while True:
        sleep(randint(1, 10) / 100)
        # shared.agentSem.wait()
        print("agent: tobacco, match")
        shared.tobacco.signal()
        shared.match.signal()


def pusher_match(shared):
    while True:
        shared.match.wait()

        shared.mutexS.lock()

        if shared.isTobacco:
            shared.isTobacco -= 1
            shared.pusherPaper.signal()
        elif shared.isPaper:
            shared.isPaper -= 1
            shared.pusherTobacco.signal()
        else:
            shared.isMatch += 1
        print(shared.isMatch)
        shared.mutexS.unlock()


def pusher_paper(shared):
    while True:
        shared.paper.wait()

        shared.mutexS.lock()

        if shared.isTobacco:
            shared.isTobacco -= 1
            shared.pusherMatch.signal()
        elif shared.isMatch:
            shared.isMatch -= 1
            shared.pusherTobacco.signal()
        else:
            shared.isPaper += 1

        shared.mutexS.unlock()


def pusher_tobacco(shared):
    while True:
        shared.tobacco.wait()

        shared.mutexS.lock()

        if shared.isPaper:
            shared.isPaper -= 1
            shared.pusherMatch.signal()
        elif shared.isMatch:
            shared.isMatch -= 1
            shared.pusherPaper.signal()
        else:
            shared.isTobacco += 1

        shared.mutexS.unlock()


def model():
    shared = Shared()

    smokers = [Thread(smoker_paper, shared),
               Thread(smoker_match, shared),
               Thread(smoker_tobacco, shared)]
    pushers = [Thread(pusher_paper, shared),
               Thread(pusher_match, shared),
               Thread(pusher_tobacco, shared)]
    agents = [Thread(agent_1, shared),
              Thread(agent_2, shared),
              Thread(agent_3, shared)]

    for t in smokers+agents+pushers:
        t.join()


if __name__ == "__main__":
    model()
