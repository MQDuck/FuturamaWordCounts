import argparse
import json
import math
import os
import re

import nltk

from tqdm import tqdm

from StemTable import StemTable
from utils import split_line


def get_grouper():
    if args.grouper == 'porter':
        return nltk.PorterStemmer().stem
    elif args.grouper == 'lancaster':
        return nltk.LancasterStemmer().stem
    lemmatizer = nltk.WordNetLemmatizer()
    return lambda s: lemmatizer.lemmatize(s, pos='v')


def get_scorer():
    if args.scorer == 'log':
        return lambda character, stem, count: stem_table.inc(character, stem, math.log(1 + count))
    elif args.scorer == 'doc':
        return lambda character, stem, count: stem_table.inc(character, stem, 1)
    return lambda character, stem, count: stem_table.inc(character, stem, count)


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

    # words = [word.replace('—', '').replace('–', '') for word in nltk.word_tokenize(dialog)]
    words = []
    for word in nltk.word_tokenize(dialog):
        if re.search('[a-zA-Z]', word) is None:
            continue
        words.append(word.replace('—', '').replace('–', ''))
    stems = [group(word) for word in words]

    for i in range(len(stems)):
        stem = stems[i]
        if stem not in stopwords:
            if stem in character_stems:
                character_stems[stem] += 1
            else:
                character_stems[stem] = 1

            word = words[i]

            if stem in character_reverse_stems:
                character_reverse_stems[stem].add(word)
            else:
                character_reverse_stems[stem] = {word}

            if stem in reverse_stems['all']:
                reverse_stems['all'][stem].add(word)
            else:
                reverse_stems['all'][stem] = {word}


arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--grouper', '-g', type=str, choices=['porter', 'lancaster', 'wordnet'], default='porter')
arg_parser.add_argument('--scorer', '-s', type=str, choices=['log', 'doc', 'count'], default='log')
arg_parser.add_argument('--aliases', '-a', type=str, choices=['single', 'multiple', 'cornwood'],
                        default=['single', 'cornwood'], nargs='*')
args = arg_parser.parse_args()

group = get_grouper()
score = get_scorer()
stopwords = [line[:-1] if line[-1] == '\n' else line for line in open('stopwords.txt', 'r') if len(line) > 1]
aliases = {}
if 'single' in args.aliases:
    aliases.update(json.load(open('aliases_single.json', 'r', encoding='utf8')))
if 'multiple' in args.aliases:
    aliases.update(json.load(open('aliases_multiple.json', 'r', encoding='utf8')))
if 'cornwood' in args.aliases:
    aliases.update(json.load(open('aliases_cornwood.json', 'r', encoding='utf8')))
print(aliases)
os.chdir('transcripts')
transcripts = [file for file in os.listdir('.') if os.path.isfile(file)]
reverse_stems = {'all': {}}
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
                score(character, stem, count)

    json.dump(stem_table.to_tuple(), open('../stem_scores.json', 'w', encoding='utf8'))
    json.dump({character: {stem: sorted(list(words), key=lambda w: len(w)) for stem, words in stems.items()}
               for character, stems in reverse_stems.items()},
              open('../reverse_stems.json', 'w', encoding='utf8'))


if __name__ == '__main__':
    main()
