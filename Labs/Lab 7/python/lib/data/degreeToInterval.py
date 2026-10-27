# send in a scale degree and return the midi value 
def degreeToMidi(interval):
    extraOctaves = math.floor( interval / len(scale) )
    interval = interval % len(scale)
    note = scale[interval] + (base_octave + extraOctaves) * 12
    
    return note