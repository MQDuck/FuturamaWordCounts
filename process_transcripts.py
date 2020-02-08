import argparse
import json
import math
import os

import nltk
from tqdm import tqdm

from StemTable import StemTable
from utils import split_line


def get_grouper():
    if args.grouper == 'porter':
        return nltk.PorterStemmer().stem
    elif args.grouper == 'lancaster':
        return nltk.LancasterStemmer().stem
    else:
        lemmatizer = nltk.WordNetLemmatizer()
        return lambda s: lemmatizer.lemmatize(s, pos='v')


def add_line(character, dialog, character_lines):
    if character in character_lines:
        character_lines[character].append(dialog)
    else:
        character_lines[character] = [dialog]


def add_stems(character, dialog, transcript_stems):
    if character in transcript_stems:
        character_stems = transcript_stems[character]
    else:
        character_stems = {}
        transcript_stems[character] = character_stems

    if character in reverse_stems:
        character_reverse_stems = reverse_stems[character]
    else:
        character_reverse_stems = {}
        reverse_stems[character] = character_reverse_stems

    words = [word.replace('—', '').replace('–', '') for word in nltk.word_tokenize(dialog)]
    stems = [group(word) for word in words]
    filtered_stems = [stem for stem in stems if stem not in stopwords]

    for stem in filtered_stems:
        if stem in character_stems:
            character_stems[stem] += 1
        else:
            character_stems[stem] = 1

    for i in range(len(stems)):
        stem = stems[i]
        if stem not in stopwords:
            word = words[i]
            if stem in character_reverse_stems:
                character_reverse_stems[stem].add(word)
            else:
                character_reverse_stems[stem] = {word}


arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--grouper', '-g', type=str, choices=['porter', 'lancaster', 'wordnet'], default='porter')
args = arg_parser.parse_args()

group = get_grouper()
stopwords = [line[:-1] for line in open('stopwords.txt', 'r') if len(line) > 1]
aliases_single = json.load(open('aliases_single.json', 'r', encoding='utf8'))
aliases_multiple = json.load(open('aliases_multiple.json', 'r', encoding='utf8'))
aliases_cornwood = json.load(open('aliases_cornwood.json', 'r', encoding='utf8'))
aliases = {**aliases_single, **aliases_cornwood}
os.chdir('transcripts')
transcripts = [file for file in os.listdir('.') if os.path.isfile(file)]
reverse_stems = {}
stem_table = StemTable()


def main():
    for transcript in tqdm(transcripts):
        transcript_stems = {}

        for line in open(transcript, 'r', encoding='utf8'):
            character, dialog = split_line(line)
            if len(character) != 0:
                if character in aliases:
                    for alias in aliases[character]:
                        add_stems(alias, dialog, transcript_stems)
                else:
                    add_stems(character, dialog, transcript_stems)

        for character, stems in transcript_stems.items():
            for stem, count in stems.items():
                stem_table.inc(character, stem, math.log(1 + count))

    json.dump(stem_table.to_tuple(), open('../stem_scores.json', 'w', encoding='utf8'))
    json.dump({character: {stem: sorted(list(words), key=lambda w: len(w)) for stem, words in stems.items()}
               for character, stems in reverse_stems.items()},
              open('../reverse_stems.json', 'w', encoding='utf8'))


if __name__ == '__main__':
    main()
