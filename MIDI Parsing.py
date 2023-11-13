import os
from mido import MidiFile
from Chord import Chord

import csv
import pandas as pd

import matplotlib.pyplot as plt
import random

class MIDIParser:
    data = {}
    index = []

    def __init__(self, dataPath):
        # dataPath = "maestro-v2.0.0"
        
        folders = os.listdir(dataPath)
        for folder in folders:
            # if folder.isdigit:
            if folder == "2018":
                files = os.listdir(dataPath + "/" + folder)
                c = 0
                for file in files:
                    print(str(c) + "/" + str(len(files)) + " files read in folder \"" + folder + "\"")
                    c += 1
                    if file[-4:] == "midi":
                        self.data[folder + "/" + file] = MidiFile(dataPath + "/" + folder + "/" + file)
        # print(self.data.keys())

        index = pd.read_csv("maestro-v2.0.0/maestro-v2.0.0.csv", encoding = "utf-8-sig")
        index = index.sort_values(by = "midi_filename", ignore_index = True)
        # print(index)

    def findFile(self, fileName):
        print(self.index[self.index["midi_filename"] == fileName])

    def parseSong(self, song):
        track = song.tracks[1]
        msgs = []
        for msg in track:
            if msg.type == "note_on":
                msgs.append(msg)

        tracklength = 0
        for msg in msgs:
            tracklength += msg.time
    
        timestamp = 0
        # allnotes = [[0 for i in range(128)] for j in range(tracklength + 1)]
        currnotes = [0 for i in range(128)]
        currchord = Chord()
        chords = []

        for msg in msgs:
            # print(msg)
            timestamp += msg.time
            currchord.timestamp = timestamp
            currnotes[msg.note] = int(msg.velocity != 0)

            for note in range(len(currnotes)):
                if currnotes[note] == 1 and note not in currchord.notes:
                    # allnotes[timestamp][note] = 1
                    currchord.notes.append(note)
            
            if msg.time > 0:
                chords.append(currchord)
                currchord = Chord()

        # transpose = []
        # for i in range(len(allnotes[0])):
        #     row2 = []
        #     for row1 in allnotes:
        #         row2.append(row1[i])
        #     transpose.append(row2)
        # plt.imshow(transpose, origin = "lower")

        return chords

#------------------------------------------------------------------------------------------------------------------------

    def plotSong(self, fileName):
        chords = self.parseSong(fileName)
        times = []
        notes = []

        for chord in chords:
            for note in chord.notes:
                times.append(chord.timestamp)
                notes.append(note)

        plt.scatter(times[:100], notes[:100], c = [random.random(), random.random(), random.random()])
        plt.show()

    def plotData(self):
        c = 0
        for song in self.data.values():
            print(str(c) + "/" + str(len(self.data.values())) + " files parsed and plotted")
            c += 1

            chords = self.parseSong(song)
            times = []
            notes = []

            for chord in chords:
                for note in chord.notes:
                    times.append(chord.timestamp)
                    notes.append(note)
            # for i in range(len(chords)):
            #     for note in chords[i].notes:
            #         times.append(i)
            #         notes.append(note)
            
            plt.scatter(times[:1000], notes[:1000], color = [random.random(), random.random(), random.random()])
        plt.show()

#------------------------------------------------------------------------------------------------------------------------

# Use "dataTemp" or "maestro-v2.0.0"
# parser = MIDIParser("maestro-v2.0.0") 
# parser.plotData()