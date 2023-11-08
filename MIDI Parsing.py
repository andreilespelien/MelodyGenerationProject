import os
from mido import MidiFile
import random

dataPath = "maestro-v2.0.0"

folders = os.listdir(dataPath)
data = {}
for folder in folders:
    # if folder.isdigit:
    if folder == "2018":
        files = os.listdir(dataPath + "/" + folder)
        for file in files:
            if file[-4:] == "midi":
                data[folder + "/" + file] = MidiFile(dataPath + "/" + folder + "/" + file)
print(data.keys())

#--------------------------------------------------------------------------------

import csv
import pandas as pd

index = pd.read_csv("maestro-v2.0.0/maestro-v2.0.0.csv", encoding = "utf-8-sig")
index = index.sort_values(by = "midi_filename", ignore_index = True)
index["midi_filename"]
print(index)

for key in data.keys():
    print(index[index["midi_filename"] == key])

#--------------------------------------------------------------------------------

import matplotlib.pyplot as plt

def parse(song):
    track = song.tracks[1]
    msgs = []
    for msg in track:
        if msg.type == "note_on":
            msgs.append(msg)
    return msgs

c = 0

for song in data.values():
    print(c)
    c += 1

    parsed = parse(song)

    times = []    
    timestamp = 0
    notes = []
    currnotes = [False for i in range(128)]

    for msg in parsed:
        timestamp += msg.time
        if msg.velocity != 0 and not currnotes[msg.note]:
            currnotes[msg.note] = True
        elif msg.velocity == 0:
            currnotes[msg.note] = False
        
        for note in range(len(currnotes)):
            if currnotes[note]:
                times.append(timestamp)
                notes.append(note)
    
    plt.scatter(times[:100], notes[:100], c = [random.random(), random.random(), random.random()])
plt.show()

#--------------------------------------------------------------------------------

