"""Authors: Bc. Patrik Saly,
            Mgr. Ing. Matúš Jókay, PhD.
Copyright 2022 All Rights Reserved.
Simple implementation of scheduler.
Resources:
https://www.dabeaz.com/coroutines/Coroutines.pdf
https://realpython.com/introduction-to-python-generators/
"""
from queue import Queue
from random import randint


class Scheduler(object):
    """
    Class representing simple Scheduler
    """
    def __init__(self):
        """
        Variables:
            ready: Queue that hold tasks ready to be scheduled
            tasks: List that hold all tasks in system
        """
        self.ready = Queue()
        self.tasks = []

    def add_new(self, task):
        """
        Function to add new task
        """
        self.tasks.append(task)
        self.schedule(task)

    def schedule(self, task):
        """
         Function to schedule task - add to the Queue to run
         """
        self.ready.put(task)

    def run(self):
        """
        Function that try to run task
        """
        while self.tasks:
            task = self.ready.get()
            try:
                result = task.run()
            except StopIteration:
                print(f"ID {task.id}: Task is finished")
                self.tasks.remove(task)
                continue
            self.schedule(task)


class Task(object):
    """
    Class that represents Task Wrapper
    """
    def __init__(self, target, task_id):
        """
        Init function
        Parameters:
        target: coroutine to be wrapped by class
        task_id: id of created task
        """
        self.target = target
        self.id = task_id
        self.send_val = None

    def run(self):
        return self.target.send(self.send_val)


def task1():
    """
    Task 1
    """
    for i in range(10):
        print("Task : ID 1")
        yield


def task2():
    """
    Task 2
    """
    for i in range(5):
        print("Task : ID 2")
        yield


def task3():
    """
    Task 3
    """
    for i in range(12):
        print("Task : ID 3")
        yield


def main():
    schedule = Scheduler()

    Task1 = Task(task1(), 1)

    Task2 = Task(task2(), 2)

    Task3 = Task(task3(), 3)

    schedule.add_new(Task1)
    schedule.add_new(Task2)
    schedule.add_new(Task3)
    schedule.run()


if __name__ == "__main__":
    main()
