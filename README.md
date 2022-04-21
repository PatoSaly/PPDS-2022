# Assignment 8

## Introduction

In this assignment we had to implement example of native coroutines in Python.
For this purpose we used the python library AsyncIO.
<br>
Installation:
```pip install asyncio```

---

## Program
In our sample program, the logic lies mainly in a different call of the
``Task`` function. The functionality of the ``Task`` 
function itself consists only of sleep, which simulates the idle
waiting of the processor. 

### Asynch program: 
```python
async def task(iD, delay):
    print(f'Called: {iD}')
    await asyncio.sleep(delay)
    print(f'{iD} took {delay} seconds to execute!')


async def main():
    tasks = [task('Task1', randint(2, 5)),
             task('Task2', randint(2, 5)),
             task('Task3', randint(2, 5))]
    await asyncio.gather(*tasks)
```

In ```asynch.py``` you can see above functions that uses acyncio calls of functions.

Async version output:

<img src="/img/asynch.png">

In example output you can see that length of program execution is basically 
longest waiting time. All tasks are waiting continuously.

### Synch program: 
```python
def task(iD, delay):
    print(f'Called: {iD}')
    time.sleep(delay)
    print(f'{iD} took {delay} seconds to execute!')


def main():
    tasks = [task('Task1', randint(2, 5)),
             task('Task2', randint(2, 5)),
             task('Task3', randint(2, 5))]
    for t in tasks:
        t
```

Sync version output:

<img src="/img/synch.png">

In example output you can see that length of program execution is combination
of all waiting times.

---

## Conclusion
In the program, we used a random value between 2 and 5 for the length of the wait function for the experiment. Despite the asynchronous program having a total wait time 2 seconds longer, the resulting program executed 3 seconds faster (longest wait time).
In this program we can clearly see the possible improvement in program performance using asynchronous functions.
