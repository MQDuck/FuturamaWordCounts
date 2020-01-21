import argparse
import json
import math
import os

import nltk

from utils import get_grouper


arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--grouper', '-g', type=str, choices=['porter', 'lancaster', 'wordnet'], default='porter')
arg_parser.add_argument('--nwords', '-n', type=int, default=10)
args = arg_parser.parse_args()

group = get_grouper(args)
stopwords = [line[:-1] for line in open('stopwords_frequency.txt', 'r') if len(line) > 1]
os.chdir('transcripts/processed')
transcripts = [file for file in os.listdir('.') if os.path.isfile(file)]

all_character_sums = {}
word_totals = {}
for transcript in transcripts:
    transcript_words = {}

    for character, dialogs in json.load(open(transcript, 'r', encoding='utf8')).items():
        for dialog in dialogs:
            words = [group(word) for word in nltk.word_tokenize(dialog)]
            words = [word for word in words if word not in stopwords]

            if character in transcript_words:
                character_words = transcript_words[character]
            else:
                character_words = {}
                transcript_words[character] = character_words

            for word in words:
                if word in character_words:
                    character_words[word] += 1
                else:
                    character_words[word] = 1

    for character, words in transcript_words.items():
        if character in all_character_sums:
            character_sums = all_character_sums[character]
        else:
            character_sums = {}
            all_character_sums[character] = character_sums

        for word, count in words.items():
            word_log = math.log(count + 1)
            if word in character_sums:
                character_sums[word] += word_log
            else:
                character_sums[word] = word_log

            if word in word_totals:
                word_totals[word] += word_log
            else:
                word_totals[word] = word_log

character_total_sums = {character: sum(words.values()) for character, words in all_character_sums.items()}

data = (all_character_sums, word_totals, character_total_sums)
json.dump(data, open('../../global_term_frequencies_log.json', 'w', encoding='utf8'))
