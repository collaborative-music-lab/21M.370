from scamp import *
import comms
from pynput import keyboard
import threading, math, random
from setup import *

debug = False # set to false to minimize clock lagging
index = 0

playing_chords = {}

def handle_note(note, velocity):

    button = note

    if velocity > 0:
        root = root_notes[button]
        chord_name = current_chords[button]
        intervals = chord_types[chord_name]
        chord = [root + i for i in intervals]
        handles = []
        for pitch in chord:
            h = piano.start_note(pitch, 0.8)
            handles.append(h)
        playing_chords[button] = handles

    else:

        if button in playing_chords:
            for h in playing_chords[button]:
                h.end()
            del playing_chords[button]

    
def handle_cc(num, val):
    if debug: print('cc', num, val)

    if num < 4:
        idx = int((val / 127) * (len(chord_type_list) - 1))
        chord_name = chord_type_list[idx]
        current_chords[num] = chord_name
        if debug:
            print("button", num, "chord:", chord_name)

def mainLoop():
    global index
    
    while True:
#         print("index: ", index)
        
        for i, name in enumerate(euclid):
            # i is the index (0, 1, 2, 3)
            # name is the string ("kick", "snare", etc.)
            
            if i in active_notes:
                print(i, euclid[name].sequence)
                if( euclid[name][index]):
                    print(name, ': ', euclid[name].sequence)
                    # handle synth separately
                    if name == 'synth':
                        comms.send_osc('note', synth_sequence[ index % 16 ]/127)
                        comms.send_osc('trigger', 3)
                        comms.send_osc('bob-filter', 1, 'CUTOFF', 15+random.random()*10 )
                    # handle drum vocies
                    else:
                        comms.send_osc('trigger', i)

        index = (index+1)
        wait(0.25)
    
def run_session():
    s.fork(mainLoop)
    s.wait_forever()

threading.Thread(target=run_session).start()

s.register_midi_listener(comms.esp32_midi_port, comms.handle_midi)
comms.handle_cc = handle_cc
comms.handle_note = handle_note

# initialize some synth parameters:
comms.send_osc( 'bwl-osc', 2, 'FM', 10)




