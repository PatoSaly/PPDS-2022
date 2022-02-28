# Assignment 2

## Task 1

In Task 1 we implemented simple barrier that was not reusable. We used Semaphore, to get expecter result. Barrier is implemented in class SimpleBarrier. You can see code in file `cv2_1.py`


## Task 2

In Task 2 we implemented reusable barrier. To get expexted result and working reusable barrier in cycle, we have to declare two diferent instances of SimpleBarrier class from Task 1. Class declaration is a bit different to successfully fulfil expectation to simply change implementation strategy from Semaphore to Event. This change can be aquired by adding comment to certain instrunction in program.

##### Use of Semaphore

```
    def __init__(self, N):
        self.N = N
        self.C = 0
        self.M = Mutex()
        # self.T = Event()
        self.T = Semaphore(0)
```

##### Use of Event

```
    def __init__(self, N):
        self.N = N
        self.C = 0
        self.M = Mutex()
        self.T = Event()
        # self.T = Semaphore(0)

```

In our program we separated two parts with two different barriers. 

```
while True:
        rendezvous(thread_name)
        barrier1.wait()
        ko(thread_name)
        barrier2.wait()
```

You can see code in file `cv2_2.py`


## Task 3

Task 3 is counting **The Fibonacci sequence** with using multrile threads. In our enviroment we were not able to succesfully repeat mistake of concurent programming. We had issues with using wait() function  on barriers while computing Fibonacci numbers. It means that Task 3 is not implemented completelty. You can see code in file `cv2_3.py`
