from random import randint
from time import sleep
from fei.ppds import Semaphore, Thread, print


PHIL_NUM = 5


def phil(forks, footman, p_id):
    sleep(randint(4, 10)/100)

    while True:
        think(p_id)
        get_forks(forks, footman, p_id)
        eat(p_id)
        put_forks(forks, footman, p_id)


def think(p_id):
    print(f'{p_id}: thinking')
    sleep(randint(3, 6)/100)


def eat(p_id):
    print(f'{p_id}: eating')
    sleep(randint(3, 6)/100)


def get_forks(forks, footman, p_id):
    footman.wait()
    print(f'{p_id}: try to get forks')
    forks[p_id].wait()
    # index can exceed range - mod PHIL_NUM
    forks[(p_id + 1) % PHIL_NUM].wait()
    print(f'{p_id}: taken forks')


def put_forks(forks, footman, p_id):
    forks[p_id].signal()
    forks[(p_id + 1) % PHIL_NUM].signal()
    print(f'{p_id} put forks')
    footman.signal()


def main():
    forks = [Semaphore(1) for _ in range(PHIL_NUM)]
    footman = Semaphore(PHIL_NUM - 1)

    phils = [Thread(phil, forks, footman, p_id) for p_id in range(PHIL_NUM)]


if __name__ == "__main__":
    main()
