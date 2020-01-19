import argparse
import json
import math
import os

import nltk

from utils import remove_brackets, get_grouper

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--grouper', '-g', type=str, choices=['porter', 'lancaster', 'wordnet'], default='porter')
arg_parser.add_argument('--nwords', '-n', type=int, default=10)
args = arg_parser.parse_args()

group = get_grouper(args)
stopwords = [line[:-1] for line in open('stopwords_doc.txt', 'r') if len(line) > 1]

os.chdir('transcripts')
transcripts = [file for file in os.listdir('.') if os.path.isfile(file)]

all_character_counts = {}
word_totals = {}
for transcript in transcripts:
    transcript_character_words = {}

    for line in open(transcript, 'r', encoding='utf8'):
        colon = line.find(':')
        if colon != -1:
            line = line.lower()
            character = line[:colon]
            dialog = remove_brackets(line[colon + 1:])
            words = [group(word) for word in nltk.word_tokenize(dialog)]
            words = [word for word in words if word not in stopwords]

            if character in transcript_character_words:
                character_set = transcript_character_words[character]
            else:
                character_set = set()
                transcript_character_words[character] = character_set

            for word in words:
                character_set.add(word)

    for character, words in transcript_character_words.items():
        if character in all_character_counts:
            character_counts = all_character_counts[character]
        else:
            character_counts = {}
            all_character_counts[character] = character_counts

        for word in words:
            if word in character_counts:
                character_counts[word] += 1
            else:
                character_counts[word] = 1

            if word in word_totals:
                word_totals[word] += 1
            else:
                word_totals[word] = 1

character_total_words = {}
for character, words in all_character_counts.items():
    total = 0
    for word, count in words.items():
        total += count
    character_total_words[character] = total

data = (all_character_counts, word_totals, character_total_words)
json.dump(data, open('../global_term_frequencies_doc.json', 'w'))
