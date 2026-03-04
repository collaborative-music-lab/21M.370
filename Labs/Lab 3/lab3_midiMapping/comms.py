from scamp import *
from pythonosc.udp_client import SimpleUDPClient
from session import s
    
port = 5005
osc = SimpleUDPClient("127.0.0.1", port)
print("starting session on port", port)

print_available_midi_input_devices()
esp32_midi_port = 1 #change to the current port for your system

def handle_note(note, velocity): pass
def handle_note(note, velocity): pass

def handle_midi(message):
    # We can change this function to process our midi messages
    msg_type = (message[0] >> 4 )
    if msg_type == 9:
        handle_note(message[1], 0)
    elif msg_type == 8:
        handle_note(message[1], number[2])
    elif msg_type == 11:
        handle_cc(message[1], message[2])             
    else:
        print('other', msg_type, message[1], message[2])



# function definitions
# function definitions
def send_osc(address, *args):
    arg_ordered = args
    if len(args) == 1 and isinstance(args[0], (list, tuple)):
        args = tuple(args[0])
    if len(args) == 3:
        a, b, c = args
        arg_ordered = [b,c,a]  # define order
    else:
        arg_ordered = list(args)
    osc.send_message("/sendto",address)
    osc.send_message("/message", list(arg_ordered))
    
send_osc('/test', 0)
