"""Authors: Bc. Patrik Saly
Copyright 2022 All Rights Reserved.
Implementation of simple async program
"""

import asyncio
import time
from random import randint


async def task(iD, delay):
    """
    Function that simulates running program with sleep
    Parameters:
        iD: Task name for identification
        delay: length of function sleep - random int in given range
    """
    print(f'Called: {iD}')
    await asyncio.sleep(delay)
    print(f'{iD} took {delay} seconds to execute!')


async def main():
    tasks = [task('Task1', randint(2, 5)), task('Task2', randint(2, 5)), task('Task3', randint(2, 5))]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    time1 = time.perf_counter()
    # calling main asynch function
    asyncio.run(main())
    time2 = time.perf_counter()
    print(f'Program ended in {time2 - time1:0.2f} seconds.')
