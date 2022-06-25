# System includes
import os
import sqlite3
from jamdict import Jamdict
from gtts import gTTS

# Allow audio files to be overwritten
OVERWRITE_AUDIO = 0

# Define the path to the Anki SQLite collection
if os.name == "nt":
    PROFILE_HOME = os.path.expandvars(r"%APPDATA%\Anki2\User 1") 
else:
    PROFILE_HOME = os.path.expanduser("~/.local/share/Anki2/User 1") 

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

    def remGrammar(self, meaningStr):
        ret = ''
        start = meaningStr.find('((')
        end = meaningStr.rfind('))') + 1
        if end == 0:
            end -= 1
        for i in range(len(meaningStr)):
            if i < start or i > end:
                ret += meaningStr[i]
        return ret

    def set_english(self):
        jmd = Jamdict()
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
                        self.english += self.remGrammar(str(s))

    def set_english_from_kana(self):
        jmd = Jamdict()
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
                        self.english += self.remGrammar(str(s))

    def set_example(self):

        """ create a database connection to a SQLite database """
        try:
            conn = sqlite3.connect("tatoeba/japTatoeba.db")
        except sqlite3.Error as e:
            print(e)
            print("Connection to sentence database failed.")
            exit()


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