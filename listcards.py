import sys, os

# Load Anki library
sys.path.append("anki") 
from anki.storage import Collection
from anki.sched import Scheduler

# Define the path to the Anki SQLite collection
PROFILE_HOME = os.path.expanduser("~/.local/share/Anki2/User 1") 
cpath = os.path.join(PROFILE_HOME, "collection.anki2")

# Load the Collection
col = Collection(cpath, log=True) # Entry point to the API

# Use the available methods to list the notes
for cid in col.findNotes('deck:GenTest'): 
    note = col.getNote(cid)
    print(note.fields[0], note.fields[1])
    print(note.fields[2])
    print(note.fields[3])
    print(note.fields[4])
    print(note.fields[5])
    print(note.fields[6])
    print('-'*40)