class Fibonacci(object):
    def __init__(self, limit):
        self.a = 0
        self.b = 1
        self.cnt = 1
        self.limit = limit

    def __next__(self):
        if self.cnt > self.limit:
            raise StopIteration

        self.a, self.b = self.b, self.a+self.b
        self.cnt += 1

        return self.b
        
    def __iter__(self):
        return self


def f(limit):
    cnt = 1
    a, b = 0, 1
    while True:
        if cnt > limit:
            return
            #raise GeneratorExit

        a, b = b, a+b
        cnt += 1
        yield b
'''
fy = f(3)
try:
    print(next(fy))
    print(next(fy))
    print(next(fy))
    print(next(fy))
except StopIteration:
    print('generovanie f je vycerpane')
'''


def cat(f, next_fnc):
    next(next_fnc)
    for line in f:
        #print('cat')
        next_fnc.send(line)
    next_fnc.close()


def grep(substr, next_fnc):
    next(next_fnc)
    try:
        while True:
            #print('grep')        
            line = (yield)
            next_fnc.send(line.count(substr))
    except GeneratorExit:
        next_fnc.close()


def wc(substr):
    cnt = 0
    try:
        while True:
            #print('wc')
            cnt += (yield)
    except GeneratorExit:
        print(substr, cnt)


def dispatch(greps):
    for g in greps: next(g)
    try:
        while True:
            line = (yield)
            for g in greps:
                g.send(line)
    except GeneratorExit:
        for g in greps: g.close()


f = open('test.py')
substr = ['b', 'while', 'complain']
greps = []

for s in substr:
    w = wc(s)
    g = grep(s, w)
    greps.append(g)

d = dispatch(greps)    
cat(f, d)
