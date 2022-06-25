import os

# Load Anki library
from anki.storage import Collection

# Define the path to the Anki SQLite collection
if os.name == "nt":
    PROFILE_HOME = os.path.expandvars(r"%APPDATA%\Anki2\User 1") 
else:
    PROFILE_HOME = os.path.expanduser("~/.local/share/Anki2/User 1") 
cpath = os.path.join(PROFILE_HOME, "collection.anki2")

# Load the Collection
col = Collection(cpath, log=True) # Entry point to the API

# Use the available methods to list the notes
for cid in col.find_notes("deck:GenTest"): 
    note = col.get_note(cid)
    print(note.fields[0], note.fields[1])
    print(note.fields[2])
    print(note.fields[3])
    print(note.fields[4])
    print(note.fields[5])
    print(note.fields[6])
    print('-'*40)