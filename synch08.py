"""Authors: Bc. Patrik Saly
Copyright 2022 All Rights Reserved.
Implementation of simple async program
"""

import time
from random import randint


def task(iD, delay):
    print(f'Called: {iD}')
    time.sleep(delay)
    print(f'{iD} took {delay} seconds to execute!')


def main():
    tasks = [task('Task1', randint(2, 5)), task('Task2', randint(2, 5)), task('Task3', randint(2, 5))]
    for t in tasks:
        t


if __name__ == "__main__":
    time1 = time.perf_counter()
    main()
    time2 = time.perf_counter()
    print(f'Program ended in {time2 - time1:0.2f} seconds.')
