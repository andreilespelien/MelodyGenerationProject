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
            if folder.isdigit:
                print(folder)
            # if folder == "2018":
                files = os.listdir(dataPath + "/" + folder)
                c = 0
                for file in files:
                    print(c)
                    c += 1
                    if file[-4:] == "midi":
                        self.data[folder + "/" + file] = MidiFile(dataPath + "/" + folder + "/" + file)
        print(self.data.keys())

        index = pd.read_csv("maestro-v2.0.0/maestro-v2.0.0.csv", encoding = "utf-8-sig")
        index = index.sort_values(by = "midi_filename", ignore_index = True)
        index["midi_filename"]
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
            # allnotes[timestamp] = currnotes
            print(currnotes.count(1))

            # print(msg)
            for note in range(len(currnotes)):
                # print(timestamp)
                if currnotes[note] == 1 and note not in currchord.notes:
                    currchord.notes.append(note)
                    # print(note)
            
            if msg.time > 0:
                chords.append(currchord)
                currchord = Chord()

        # plt.imshow(allnotes[938:939])
        # transpose = []
        # for i in range(len(allnotes[0])):
        #     row = []
        #     for j in allnotes[928:948]:
        #         row.append(j[i])
        #         transpose.append(row)
        # plt.imshow(transpose)
        # plt.show()

        for chord in chords[:100]:
            print(len(chord.notes), chord.timestamp)
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
            print(c)
            c += 1

            chords = self.parseSong(song)
            times = []
            notes = []

            for chord in chords:
                for note in chord.notes:
                    times.append(chord.timestamp)
                    notes.append(note)

            print(times[:100])
            
            plt.scatter(times[:100], notes[:100], c = [random.random(), random.random(), random.random()])
        plt.show()


parser = MIDIParser("dataTemp") # maestro-v2.0.0
parser.plotData()