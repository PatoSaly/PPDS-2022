# Assignment 6
### In assignment 6 we implemented a barbers and multiple customers problem without strict FIFO queue

## Basic problem description
- 2 rooms in barbershop
  - waiting room (W places)
  - room for barber (B barbers, one customer at a time)
- if there are no customers, barber is waiting
- if customer comes to barbershop
  - if there is no room in waiting room, he leaves
  - if there is room in waiting room, he is waiting
- if there is no customer in barber room, one from waiting room goes in there
- **The problem consists of coordinating the customer and the barber.**

>We aim for concurrent execution of cutting hair function.

For this purpose, we used synchronization functions to jointly start and end the haircut by both the barber and the customer.

## Barber
The barber waits for the customer to arrive (`customer.signal`) and then tells to customer that he is ready (`barber.signal`). He starts to cut the hair and when he is finished he waits for the customer's signal that he is satisfied (`customerDone.signal`). The last thing is that the barber signals to the customer that he has completed all the operations (`barberDone.signal`).

Barber use help function `cut_hair` that simulates barber cutting customer's hair.

## Customer
The customer first finds out if there is enough space in the barber shop and if yes he enters the barber shop, if not he leaves and comes back later (`balk`). 

The customer signals that he is ready (`customer.signal`) and is waiting for the barber. After the signal from the barber, the get_cut_hair function is called. Then the customer signals that he is satisfied with the haircut (`customerDone.signal`) and waits for the barber to complete all the operations.

The number of customers in the waiting room is provided by the `customers_count` variable and its integrity is guaranteed by the mutex.

Thread customer use help functions `balk`, `get_cut_hair` and `grow_hair` to help simulate system.
