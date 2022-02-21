# PPDS-2022 - Assignment 1

<br />

## Inroduction
The basic problem of this assignment is that we need to perform 
an **operation** that has **two steps** with **more than one thread**
at the same time. In order to do this, we need to modify the code
so that the two-step **operation is executed atomically**.
To achieve this, we use a **mutex lock**. 

<br />

### Parts of operation
1. Increase the value of variable in array on a particular index by one
2. Increace index by one

<br />

## Programs
In this Assignment we chose two different methods to achieve atomicity of the operation. 
The difference is in the amount of code covered by the lock.

<br />

### Encapsulation of the entire problematic function
This method is used in file ```cv01_1.py```. Main function that is used to make
calculation and potentially cause problems with multiple threads is in function ```do_count```.
While using this method, we call lock in the beginning of function and release
lock when execution of function is finished. 

```
do_count()
   mutex.lock()
   #execution of function
   mutex.unlock()
```

<br />

### Encapsulation of the minimal necessary part
This method is used in file ```cv01_2.py```. Second method seems like better solution.
We put between lock just necessary part of code that need to be executed atomically. 
In our minimalistic example we left out just the while loop. 
```
do_count()
   while True:
       mutex.lock()
       #execution of function
       mutex.unlock()
```

<br />

## Conclusion
Due to the version of the Python programming language we were using,
we were forced to insert the execution error into the program ourselves.
It is represented by putting threads to sleep for a random time during 
the program execution. By using a lock, we successfully prevented two threads
from working with the same data variable at the same time in both cases.
However, due to the use of sleep, we had to use a smaller array size that
was incremented and the difference between the methods did not affect the
speed of the program. We think, that
significant difference might be visible at array length from 1 000 000.
