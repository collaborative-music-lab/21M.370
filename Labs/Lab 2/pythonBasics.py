from scamp import Session, wait
from pythonosc.udp_client import SimpleUDPClient
from pynput import keyboard
import random
import math

port = 5005
s = Session(tempo=120)
osc = SimpleUDPClient("127.0.0.1", port)
print("starting session on port", port)

#global variable

# 1. Global state
def melody():
    while True:
        osc.send_message("/sendto","newNote")
        osc.send_message("/message", 0)

        wait(1) 
        
s.fork(melody)
s.wait_forever()

