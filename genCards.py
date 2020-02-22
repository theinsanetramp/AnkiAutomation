import sys, os
import csv
import re
from jamdict import Jamdict
import webbrowser
import sqlite3
from sqlite3 import Error
from gtts import gTTS

NO_ANKI = 0
OVERWRITE_AUDIO = 0

PROFILE_HOME = os.path.expanduser("~/.local/share/Anki2/User 1") 

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None

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
        if japanese == '':
            print("No Kanji for", reading, "- generating from reading alone")
            print()
            self.japanese = reading
            self.reading = ''
            self.set_english_from_kana()
        else:
            self.japanese = japanese
            self.reading = reading
            self.set_english()
        self.set_example()
        self.firstEnc = firstEnc
        self.set_audio()
        self.notes = ''

    def set_english(self):
        self.english = ''
        self.isVerb = 0
        results = jmd.lookup(self.japanese)
        for entry in results.entries:
            # print(entry)
            # print()
            for self.kana in entry.kana_forms:
                if self.reading == str(self.kana):
                    if self.english:
                        self.english += '; '
                    for idx, s in enumerate(entry.senses):
                        if idx > 0:
                            self.english += '; '
                        if (str(s).find('Godan verb') != -1) or (str(s).find('Ichidan verb') != -1):
                            self.isVerb = 1
                        self.english += remGrammar(str(s))

    def set_english_from_kana(self):
        self.english = ''
        self.isVerb = 0
        results = jmd.lookup(self.japanese)
        for entry in results.entries:
            # print(entry)
            # print()
            for noEntries, self.kana in enumerate(entry.kana_forms):
                if self.japanese == str(self.kana):
                    if self.english:
                        self.english += '; '
                    for idx, s in enumerate(entry.senses):
                        if idx > 0 and self.english:
                            self.english += '; '
                        if str(s).find('verb') != -1 and str(s).find('verb suru') == -1 and str(s).find('adverb') == -1:
                            self.isVerb = 1
                        self.english += remGrammar(str(s))

    def set_example(self):
        cur = conn.cursor()
        sql = "SELECT * FROM sentences WHERE LENGTH(japanese) <= 35 AND japanese LIKE ?"
        cur.execute(sql, ('%'+self.japanese+'%',))
        rows = cur.fetchall()
        try: 
            self.exJap = rows[0][1]
            self.exEng = rows[0][2]
        except:
            if(self.isVerb):
                cur.execute(sql, ('%'+self.japanese[:-1]+'%',))
                rows = cur.fetchall()
                print("No example sentence for", self.japanese, "- trying", self.japanese[:-1])
                print()
                try:
                    self.exJap = rows[0][1]
                    self.exEng = rows[0][2]
                except:
                    cur.execute(sql, ('%'+self.reading+'%',))
                    rows = cur.fetchall()
                    print("No example sentence for", self.japanese[:-1], "- trying", self.reading)
                    print()
                    try:
                        self.exJap = rows[0][1]
                        self.exEng = rows[0][2]
                    except:
                        cur.execute(sql, ('%'+self.reading[:-1]+'%',))
                        rows = cur.fetchall()
                        print("No example sentence for", self.reading, "- trying", self.reading[:-1])
                        print()
                        try:
                            self.exJap = rows[0][1]
                            self.exEng = rows[0][2]
                        except:
                            print("No example sentence for", self.reading[:-1])
                            print()
                            self.exJap = ''
                            self.exEng = ''
            else:
                if self.reading:
                    cur.execute(sql, ('%'+self.reading+'%',))
                    rows = cur.fetchall()
                    print("No example sentence for", self.japanese, "- trying", self.reading)
                    print()
                    try:
                        self.exJap = rows[0][1]
                        self.exEng = rows[0][2]
                    except:
                        print("No example sentence for", self.reading)
                        print()
                        self.exJap = ''
                        self.exEng = ''
                else:
                    print("No example sentence for", self.japanese)
                    print()
                    self.exJap = ''
                    self.exEng = ''


    def set_audio(self):
        self.audio = self.japanese+'.mp3'
        exists = os.path.isfile(PROFILE_HOME+'/collection.media/'+self.audio)
        if exists and not OVERWRITE_AUDIO:
            print("Audio file", self.audio, "already exists - no audio generated")
            print()
        else:
            if self.exJap:
                tts = gTTS(self.exJap, lang="ja") 
                tts.save(PROFILE_HOME+'/collection.media/'+self.audio)
            else:
                tts = gTTS(self.japanese, lang="ja") 
                tts.save(PROFILE_HOME+'/collection.media/'+self.audio)
        self.audio = '[sound:' + self.audio + ']'

    def set_notes(self, notes):
        self.notes = notes


# List of all words
words = []
jmd = Jamdict()
print()
try:
    conn = create_connection("tatoeba/japTatoeba.db")
except:
    print("Connection to sentence database failed.")


with open('newCards.txt', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    new_source = 1
    for row in csv_reader:
        if new_source:
            FE = row[0]
            new_source = 0
        else:
            if row:
                words.append(Word(row[0],row[1],FE))
            else:
                new_source = 1
        line_count += 1
    print()
    print(f'Processed {line_count} lines.')

print('-'*40)
for word in words:
    print(word.japanese, word.reading)
    print(word.english)
    print(word.exJap)
    print(word.exEng)
    print(word.firstEnc)
    print(word.audio)
    print('-'*40)

if NO_ANKI:
    print()
    print("NO_ANKI = 1")
    print("0 cards created.")
else:
    # Load Anki library
    sys.path.append("anki") 
    from anki.storage import Collection
    from anki.sched import Scheduler

    # Define the path to the Anki SQLite collection
    cpath = os.path.join(PROFILE_HOME, "collection.anki2")

    # Load the Collection
    col = Collection(cpath, log=True) # Entry point to the API

    # Set the model
    modelBasic = col.models.byName('NihongoShark.com: My Vocabulary')
    col.decks.current()['mid'] = modelBasic['id']

    # Get the deck
    deck = col.decks.byName("GenTest")
    doneCards = 0
    print()

    for word in words:
        if not col.findNotes('deck:GenTest "Target Japanese Word":'+word.japanese):
            # Instantiate the new note
            note = col.newNote()
            note.model()['did'] = deck['id']

            note.fields[0] = word.japanese 
            note.fields[1] = word.reading
            note.fields[2] = word.english
            note.fields[3] = word.exJap
            note.fields[4] = word.exEng
            note.fields[5] = word.firstEnc
            note.fields[6] = word.audio

            col.addNote(note)
            doneCards += 1
        else:
            print(word.japanese, "already exists in deck - card not loaded")
            print()

    print(doneCards, 'cards created.')
    col.save()