import argparse
import json
import math
import os
import re

import nltk
from tqdm import tqdm

from WordTable import WordTable
from utils import get_grouper


def remove_brackets(s):
    parts = re.split('\[|\]', s)
    s = ''.join([parts[i] for i in range(len(parts)) if i % 2 == 0])
    parts = re.split('\(|\)', s)
    s = ''.join([parts[i] for i in range(len(parts)) if i % 2 == 0])
    parts = re.split('<|>', s)
    return ''.join([parts[i] for i in range(len(parts)) if i % 2 == 0])


# noinspection PyShadowingNames
def add_line(character, dialog, character_lines):
    if character in character_lines:
        character_lines[character].append(dialog)
    else:
        character_lines[character] = [dialog]


def add_words(character, dialog, transcript_words):
    if character in transcript_words:
        character_words = transcript_words[character]
    else:
        character_words = {}
        transcript_words[character] = character_words

    words = [group(word) for word in nltk.word_tokenize(dialog)]
    words = [word for word in words if word not in stopwords]
    for word in words:
        if word in character_words:
            character_words[word] += 1
        else:
            character_words[word] = 1

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--grouper', '-g', type=str, choices=['porter', 'lancaster', 'wordnet'], default='porter')
args = arg_parser.parse_args()

group = get_grouper(args)
stopwords = [line[:-1] for line in open('stopwords_frequency.txt', 'r') if len(line) > 1]
aliases_single = json.load(open('aliases_single.json', 'r', encoding='utf8'))
aliases_multiple = json.load(open('aliases_multiple.json', 'r', encoding='utf8'))
aliases_cornwood = json.load(open('aliases_cornwood.json', 'r', encoding='utf8'))
aliases = {**aliases_single, **aliases_cornwood}
os.chdir('transcripts')
transcripts = [file for file in os.listdir('.') if os.path.isfile(file)]
word_table = WordTable()

for transcript in tqdm(transcripts):
    transcript_words = {}

    for line in open(transcript, 'r', encoding='utf8'):
        line = remove_brackets(line)
        colon = line.find(':')
        if colon != -1:
            character = line[:colon].lower().strip()
            dialog = line[colon + 1:].lower()
            if character in aliases:
                for alias in aliases[character]:
                    add_words(alias, dialog, transcript_words)
            else:
                add_words(character, dialog, transcript_words)

    for character, words in transcript_words.items():
        for word, count in words.items():
            word_table.inc(character, word, math.log(1 + count))

json.dump(word_table.to_tuple(), open('../word_scores.json', 'w', encoding='utf8'))
