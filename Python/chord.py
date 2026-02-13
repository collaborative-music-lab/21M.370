from scamp import *
from pythonosc.udp_client import SimpleUDPClient
from pynput import keyboard 

port = 5005
s = Session(tempo=120)
pd = s.new_osc_part("synth", port=port)
osc = SimpleUDPClient("127.0.0.1", port)
print("starting session on port", port)

# 1. Global state
index = 0
beat_length = 2
majorScale = [0,2,4,5,7,9,11]

# function definitions
def send_osc(address, *args):
    osc.send_message("/sendto",address)
    osc.send_message("/message", list(args))

def playChords():
    global index
    chord = [ majorScale[index%7],majorScale[(index+2)%7],majorScale[(index+4)%7]] 
    while True:
        chord = [ majorScale[index%7],majorScale[(index+2)%7],majorScale[(index+4)%7]]
        for i in range(3):
            cv = chord[i] * 1/127
            send_osc("voice" + str(i+1), cv)
            
        print("playing", index, chord)
        index = (index+1)%8
        wait(beat_length)

# call functions
s.fork(playChords)
s.wait_forever()


