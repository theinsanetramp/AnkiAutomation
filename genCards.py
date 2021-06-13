# System includes
import sys, os
import csv
import re
import webbrowser
from anki import Collection

# Project includes
import word as wd

# Set to 1 to do a dry run without anything loading into anki
NO_ANKI = 0

words = []
print()

# Get the words that need new cards from txt file
with open('newCards.txt', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    new_source = 1

    # Generate card fields for each word
    for row in csv_reader:
        if new_source:
            FE = row[0]
            new_source = 0
        else:
            if row:
                words.append(wd.Word(row[0],row[1],FE))
            else:
                new_source = 1
        line_count += 1
    print()
    print('Processed {line_count} lines.')

# Print card fields generated
print('-'*40)
for word in words:
    print(word.japanese, word.reading)
    print(word.english)
    print(word.exJap)
    print(word.exEng)
    print(word.firstEnc)
    print(word.audio)
    print('-'*40)

# If expected to do so, export to anki
if NO_ANKI:
    print()
    print("NO_ANKI = 1")
    print("0 cards created.")
else:
    # Define the path to the Anki SQLite collection
    cpath = os.path.join(wd.PROFILE_HOME, "collection.anki2")

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
        if not col.findNotes('deck:GenTest *Word:'+word.japanese):
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