"""Experiment, that shows how different parameters in
   Producer, Consumer system affect
   result - number of produced items
"""

from fei.ppds import Semaphore, Mutex, print, Thread
from random import randint
from time import sleep
import pandas as pd
import plotly.express as px
import csv
import time


class Shared:
    def __init__(self, n):
        self.finished = False
        self.mutex = Mutex()
        self.free = Semaphore(n)
        self.items = Semaphore(0)


def producer(shared, time_of_production):
    global count
    while True:
        # production
        sleep(time_of_production)
        count += 1
        shared.free.wait()
        if shared.finished:
            break
        shared.mutex.lock()
        # store product in warehouse
        sleep(randint(1, 10) / 100)
        shared.mutex.unlock()
        shared.items.signal()


def consumer(shared):
    while True:
        shared.items.wait()
        if shared.finished:
            break
        shared.mutex.lock()
        # get product from Warehouse
        sleep(randint(1, 10) / 100)
        shared.mutex.unlock()
        # consume product
        sleep(randint(1, 5) / 10)


def draw_output():
    df = pd.read_csv('out.cvs')

    print(df.describe())

    fig = px.scatter_3d(df,
                        x='time_of_production',
                        y='n_producers',
                        z='avg_count')
    fig.update_layout(
        title="Producer, Consumer scatter graph",
        font=dict(
            family="sans-serif",
            size=14,
            color="black"
        )
    )

    fig.show()


"""Measured values are Number of producers,
   number of comsumers, time of production
"""
output = []
count = 0
for j in range(1, 100):
    # change system settings
    n_producers = j
    n_consumers = j
    time_of_production = randint(1, 10) / j

    out = []

    for i in range(10):
        s = Shared(1000)
        count = 0
        time1 = time.perf_counter()
        c = [Thread(consumer, s) for _ in range(n_consumers)]
        p = [Thread(producer, s, time_of_production)
             for _ in range(n_producers)]

        sleep(5)
        s.finished = True

        time2 = time.perf_counter()
        s.items.signal(1000)
        s.free.signal(1000)
        [t.join() for t in c+p]

        delta_time = time2 - time1

        out.append(count / delta_time)

    avg = sum(out) / len(out)
    print(f"Test c.{j}, n_producers:{n_producers},"
          f" time_of_production: {time_of_production}, avg_count: {avg}")
    output.append([n_producers, time_of_production, avg])

# write output to file
header = ["n_producers", "time_of_production", "avg_count"]
with open('out.cvs', 'w', newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    for line in output:
        writer.writerow(line)

draw_output()
