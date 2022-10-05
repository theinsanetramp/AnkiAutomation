# AnkiAutomation

Automating Japanese Anki flashcards using the Anki API

## Installation

The Python packages required for this project are managed using Poetry. Install Poetry as instructed [here](https://python-poetry.org/docs/):

```sh
# Linux, WSL installation
curl -sSL https://install.python-poetry.org | python3 -
# Windows (Powershell) installation
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

Poetry can then be used to create the Python virtual environment:

```sh
poetry install
```

You must also have Anki installed and you must have the `NihongoShark.com: My Vocabulary` card template provided by [this deck](https://ankiweb.net/shared/info/993866228). Create a deck called `genTest` - this is where flashcards will be generated.

## Usage

Add new words to `newCards.txt` in the format below:

```
Word origin (where you first saw it)
Kanji,Kana
Kanji,Kana

Word origin 2 (where you first saw it)
Kanji,Kana
Kanji,Kana
```

If you wish to add a word that doesn't use kanji then simply ommit the kanji field (keeping the comma, i.e., `,Kana`). Be careful that you are using the exact same type of comma as in these instructions and that there is a empty line between the final word from one word origin and the line containing the next wrod origin.

As an example, if I wanted to make flashcards for 遅刻 and ヘルシー, which I first encountered while reading Made in Abyss, and 自動, which I first encountered while reading よつばと, I would edit `newCards.txt` to look like this:

```
Made in Abyss
遅刻,ちこく
,ヘルシー

よつばと
自動,じどう
```

To generate the flashcards you must first make sure that Anki isn't running, then run:

```sh
poetry run python genCards.py
```

Open Anki and check the `genTest` deck - the new flashcards should have been added there. It is worth checking through each flashcard to make sure the fields are correct - pay particular attention to the example sentences, as it can sometimes pick an incorrect sentence or not find one that uses the word at all. Once you are confident that the cards are correct, move them to your deck of choice for learning.

## Regenerating the example sentence database

For example sentence db generation, the `tatoeba` folder needs from [tatoeba downloads](https://tatoeba.org/en/downloads):
- sentences.csv
- links.csv

To generate the database (hopefully - I haven't run this since 2018) run:

```sh
poetry run python genSentenceDB.py
```

## TODO

 - Make overwrite audio files a command line option
 - Clean up and comment
 - い verb conjugation
 - Better definition scrubbing?
 - Partitioning of longer sentences?