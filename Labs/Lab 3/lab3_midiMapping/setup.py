from scamp import *
from session import s

def mainLoop():
    while True:
        print('foo')
        wait(0.5)

def run_session():
    print('sdfg')
    s.fork(mainLoop)
    s.wait_forever()
