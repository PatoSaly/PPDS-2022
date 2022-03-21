# Assignment 5

## Task 1 - Smokers 

In the first task, we should to discuss **favoring** certain results **according to the order in the code** 
in smokers problem.

After several tries we think that this problem can be solved by implementing strong FIFO queue in Semaphore.

Example code from lecture is in file `cv05_smokers.py`

<br>

## Task 2 - Dining Savages

In task 2 we should solve problem with multiple cooks cooking foot in the same time. Last cook should
signal that pot is full. 

In our program we extended functionality of code from lecture where more savages stars eating in the same time 
and one of them signals to cook that pot is empty. 


### Pseudocode:

```
N = NumberOfSavages
M = SizeOfPot
C = NUmberOfCooks

def main():
    shared := Shared(0)
    savages := Thread(savage) in range N
    cooks := Thread(cook) in range C  


class Shared:
    servings := m
    mutexS := Mutex()
    mutexC := Mutex()
    empty_pot := Semaphore(0)
    full_pot := Semaphore(0)
    cooks_count := 0
    b1 := SimpleBarrier(N)
    b2 := SimpleBarrier(C)


def savage(i, shared):
    while True:
        shared.b1.wait_on_barrier()
        shared.mutexS.lock()
        if shared.servings == 0:
            print("empty pot")
            shared.empty_pot.signal(C)
            shared.full_pot.wait()
        print(f"savage {i}: take from pot")
        shared.servings -= 1
        shared.mutexS.unlock()
        eat(i)


def cook(j, shared):
    while True:
        shared.empty_pot.wait()
        shared.b2.wait_on_barrier()
        
        shared.mutexC.lock()
        shared.cooks_count += 1
        shared.mutexC.unlock()

        cooking() 
        if shared.cooks_count == C:
            put_servings_to_pot()
            shared.full_pot.signal()
            shared.cooks_count := 0      
```

Some key characteristics of system:
- Savages start eating together
- Cooks start cooking together 
- First savage that dins out that pot is empty signals to cooks
- Last cook that has finished cooking signals to savages that pot is full
- Taking serving from pot is sequential (atomic thanks to mutex) operation
- Eating is parallel operation
- Cooking is parallel operation

>This program is problem of two barriers

<br>

Program works properly with various inputs (parameters of system)

### Example output - 3 savages, 3 cooks, max 2 servings in pot
```
savage 1: before dinner             [savage 1 Thread came to barrier]
savage 0: before dinner             [savage 0 Thread came to barrier]
savage 2: before dinner             [savage 2 Thread came to barrier]
savage 2: all savages are there     [all savage Threads are on barrier so they can continue]
savage 2: empty pot                 [savage 2 signals empty pot]
cook 2 waiting                      [cook 2 Thread came to barrier]
cook 1 waiting                      [cook 1 Thread came to barrier]
cook 0 waiting                      [cook 0 Thread came to barrier]
all cooks going to cook             [all savage Threads are on barrier so they can continue]
cook 0: cooking                     [cook 0 starts cooking]
cook 2: cooking                     [cook 2 starts cooking]
cook 1: cooking                     [cook 1 starts cooking]
cook 2: 2 servings -> pot           [only one cook Thread signals full pot (2 servings)]
savage 2: take from pot             [savage 2 Thread took one serving] 
savage 2: eating                    [savage 2 Thread is eating]
savage 1: take from pot             [savage 1 Thread took one serving]
savage 1: eating                    [savage 1 Thread is eating]
savage 0: empty pot                 [savage 0 signals empty pot]
.
.
.
```
Text in [...] is just an explanation and is not part of output

You can find finished task 2 in file `cv05_savages.py`
