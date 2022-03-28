"""Authors: Bc. Patrik Saly,
            Mgr. Ing. Matúš Jókay, PhD.
Copyright 2022 All Rights Reserved.
Implementation of the problem of barber and multiple customers.
"""

from fei.ppds import Thread, Mutex, Semaphore, print
from random import randint
from time import sleep


class Shared:
    """Shared object
    Init parameters:
        customers_count - counter of customers in waiting room
        mutexC - protects integrity of customer_count
        customer - customer signals to barber
        barber - barber signals to customer
        customerDone - customer signals to barber that customer is finished
        barberDone - barber signals to customer that barber is finished
    """
    def __init__(self):
        self.customers_count = 0
        self.mutexC = Mutex()

        self.customer = Semaphore(0)
        self.barber = Semaphore(0)

        self.customerDone = Semaphore(0)
        self.barberDone = Semaphore(0)


def balk(i):
    """Function that simulates customer leaving
     barbershop and returns later.
     """
    print(f'Barbershop is full! {i} will come later.')
    sleep(randint(25, 30)/100)


def get_cut_hair(i):
    """Function that simulates customer
    getting cut his hair.
    """
    print(f'Customer {i} getting his hair cut.')
    sleep(2/100)


def grow_hair(i):
    """Function that simulates customer waiting to
    grow his hair after visiting barbershop.
    """
    sleep(randint(5, 7)/10)
    print(f'Hair of customer {i} has grown.')


def customer(i, shared):
    """Function that simulates customer
    coming to barbershop and getting his hair cut.
    If there is no empty place in waiting room (W)
    customer leaves and returns later.
    """
    while True:
        shared.mutexC.lock()
        if shared.customers_count == W:
            shared.mutexC.unlock()
            balk(i)
            continue
        shared.customers_count += 1
        shared.mutexC.unlock()

        shared.customer.signal()
        shared.barber.wait()

        get_cut_hair(i)

        shared.customerDone.signal()
        shared.barberDone.wait()

        shared.mutexC.lock()
        shared.customers_count -= 1
        shared.mutexC.unlock()

        grow_hair(i)


def cut_hair(i):
    """Function that simulates barber
    cutting customer hair.
    """
    print(f'Barber {i} is cutting hair.')
    sleep(2/100)


def barber(i, shared):
    """Function that simulates barber
    waiting for customer and then cutting
    his hair.
    """
    while True:
        shared.customer.wait()
        shared.barber.signal()

        cut_hair(i)

        shared.customerDone.wait()
        shared.barberDone.signal()


def main():
    shared = Shared()
    barbers = []
    customers = []

    for i in range(1, C+1):
        customers.append(Thread(customer, i, shared))

    for j in range(1, B+1):
        barbers.append(Thread(barber, j, shared))

    for t in customers + barbers:
        t.join()


if __name__ == "__main__":
    C = 14
    B = 1
    W = 2
    main()
