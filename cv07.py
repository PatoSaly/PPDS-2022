"""Authors: Bc. Patrik Saly,
            Mgr. Ing. Matúš Jókay, PhD.
Copyright 2022 All Rights Reserved.
Simple implementation of scheduler.
"""
from queue import Queue
from random import randint


class Scheduler(object):
    def __init__(self):
        self.ready = Queue()
        self.tasks = []

    def add_new(self, task):
        self.tasks.append(task)
        self.schedule(task)

    def schedule(self, task):
        self.ready.put(task)

    def run(self):
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
    def __init__(self, target, task_id):
        self.target = target
        self.id = task_id
        self.send_val = None

    def run(self):
        return self.target.send(self.send_val)


def task1():
    for i in range(10):
        print("Task : ID 1")
        yield


def task2():
    for i in range(5):
        print("Task : ID 2")
        yield


def task3():
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
