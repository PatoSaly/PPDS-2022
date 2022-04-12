# Assignment 7
## Simple scheduler

In this assignment we implemented simple example of Scheduler. In main.py are 3
functions (tasks), that are switched by Scheduler. 

In every function is for cycle with different number of iterations. After every iteration, function waits on 
yeld until scheduler call her function run again. Thanks to different numbers of iterations we can see
how functions end in different time. Example is simle but shows how function yeld can be used to Schedule context

```
def task1():
    for i in range(10):
        print("Task : ID 1")
        yield
```
