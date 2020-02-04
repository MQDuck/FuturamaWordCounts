import argparse
import json
import math
import os

import nltk
from tqdm import tqdm

from WordTable import WordTable
from utils import get_grouper

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--grouper', '-g', type=str, choices=['porter', 'lancaster', 'wordnet'], default='porter')
args = arg_parser.parse_args()

group = get_grouper(args)
stopwords = [line[:-1] for line in open('stopwords_frequency.txt', 'r') if len(line) > 1]
os.chdir('transcripts/processed')
transcripts = [file for file in os.listdir('.') if os.path.isfile(file)]

word_table = WordTable()

for transcript in tqdm(transcripts):
    transcript_word_counts = {}

    for character, dialogs in json.load(open(transcript, 'r', encoding='utf8')).items():
        for dialog in dialogs:
            words = [group(word) for word in nltk.word_tokenize(dialog)]
            words = [word for word in words if word not in stopwords]

            if character in transcript_word_counts:
                character_word_counts = transcript_word_counts[character]
            else:
                character_word_counts = {}
                transcript_word_counts[character] = character_word_counts

            for word in words:
                if word in character_word_counts:
                    character_word_counts[word] += 1
                else:
                    character_word_counts[word] = 1

    for character, word_counts in transcript_word_counts.items():
        for word, count in word_counts.items():
            word_table.inc(character, word, math.log(1 + count))

json.dump(word_table.to_tuple(), open('../../global_term_frequencies_log.json', 'w', encoding='utf8'))
