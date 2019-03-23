import sys, os
import csv
import re
from jamdict import Jamdict
import webbrowser

def remGrammar(meaningStr):
    ret = ''
    start = meaningStr.find('((')
    end = meaningStr.rfind('))') + 1
    if end == 0:
        end -= 1
    for i in range(len(meaningStr)):
        if i < start or i > end:
            ret += meaningStr[i]
    return ret

class Word:

    def __init__(self, japanese, reading, firstEnc):
        self.japanese = japanese
        self.reading = reading
        self.english = ''
        results = jmd.lookup(japanese)
        for entry in results.entries:
            print(entry)
            print()
            for kana in entry.kana_forms:
                if reading == str(kana):
                    for idx, s in enumerate(entry.senses):
                        if idx > 0:
                            self.english += '; '
                        self.english += remGrammar(str(s))
                        idx += 1
        self.exJap = ''
        self.exEng = ''
        self.firstEnc = firstEnc
        self.audio = ''
        self.notes = ''

    def set_english(self, english):
        self.english = english

    def set_exJap(self, exJap):
        self.exJap = exJap

    def set_exEng(self, exEng):
        self.exEng = exEng

    def set_firstEnc(self, firstEnc):
        self.firstEnc = firstEnc

    def set_audio(self, audio):
        self.audio = audio

    def set_notes(self, notes):
        self.notes = notes


# List of all words
words = []
jmd = Jamdict()
print()

with open('newCards.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            FE = row[0]
        else:
            if row[1]:
                words.append(Word(row[0],row[1],FE))
            else:
                print("Searching", row[0], "on Jisho...")
                print()
                webbrowser.open_new_tab('https://jisho.org/search/' + row[0])
        line_count += 1
    print(f'Processed {line_count-1} words.')

print(len(words), 'cards created.')
print('-'*40)
for word in words:
    print(word.japanese, word.reading)
    print(word.english)
    print(word.exJap)
    print(word.exEng)
    print(word.firstEnc)
    print('-'*40)

# Load Anki library
sys.path.append("anki") 
from anki.storage import Collection
from anki.sched import Scheduler

# Define the path to the Anki SQLite collection
PROFILE_HOME = os.path.expanduser("~/.local/share/Anki2/User 1") 
cpath = os.path.join(PROFILE_HOME, "collection.anki2")

# Load the Collection
col = Collection(cpath, log=True) # Entry point to the API