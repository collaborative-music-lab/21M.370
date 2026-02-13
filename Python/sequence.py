from scamp import *
from pythonosc.udp_client import SimpleUDPClient
from pynput import keyboard
import threading
from math import sin, floor

port = 5005
s = Session(tempo=120)
osc = SimpleUDPClient("127.0.0.1", port)
print("starting session on port", port)

# 1. Global state
index = 0
beat_length = 1
sequence = [0,2,4,5,7,9,11,12]
majorScale = [0,2,4,5,7,9,11,12]
val = 0

def makeSequence(val):
    for i in range(len(sequence)):
        note = floor( (sin(val*i)+1) * 4)
        print(note)
        sequence[i] = majorScale[ floor(note) % len(majorScale) ]
    print(sequence)
    
    
# function definitions
def send_osc(address, *args):
    osc.send_message("/sendto",address)
    osc.send_message("/message", list(args))

def playSequence():
    global index
    cv = 0
    while True:
        cv = sequence[index] * 1/127
        send_osc("voice1", cv)
        
        cv = sequence[ (index+2)% len(sequence) ] * 1/127
        send_osc("voice2", cv)
        
        cv = sequence[ (index+4)% len(sequence) ] * 1/127
        send_osc("voice3", cv)
        
        cv = (sequence[ (index+6)% len(sequence) ] + 12) * 1/127
        send_osc("voice4", cv)
#         print("playing", index, sequence[index])

        index = (index+1) % len(sequence)
        beat_length = [.5,.75,1][index%3]
        wait(beat_length)


def run_session():
    s.fork(playSequence)
    s.wait_forever()

threading.Thread(target=run_session).start()


