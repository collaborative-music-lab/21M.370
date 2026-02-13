from scamp import Session, wait
from pythonosc.udp_client import SimpleUDPClient
from pynput import keyboard 

port = 5005
s = Session(tempo=120)
pd = s.new_osc_part("synth", port=port)
osc = SimpleUDPClient("127.0.0.1", port)
print("starting session on port", port)

# 1. Global state
current_pitch = 60 
# Pitch map: keys 1, 2, 3, 4 assign different notes
pitch_map = {
    '1': 60, # C
    '2': 62, # D
    '3': 64, # E
    '4': 67  # G
}

# 2. Define the background listener function
def on_press(key):
    global current_pitch
    try:
        # Check if the alphanumeric key is in our map
        k = key.char
        if k in pitch_map:
            current_pitch = pitch_map[k]
            print(f"-> Switched pitch to: {current_pitch}")
    except AttributeError:
        # Handle special keys (shift, ctrl, etc) if needed
        pass

# 3. Start the listener in the background
listener = keyboard.Listener(on_press=on_press)
listener.start()

def melody():
    while True:
        # start_note sends the OSC message and moves to the next line IMMEDIATELY
        osc.send_message("/sendto","bwl-osc")
        osc.send_message("/message", list(["PITCH", current_pitch, 1]))

        wait(1)  # Wait the remainder of the beat (0.7 + 0.3 = 1 beat totalprint("making forks")
        
s.fork(melody)
s.wait_forever()
