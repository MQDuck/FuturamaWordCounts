import argparse
import json
import os

import nltk

from utils import get_grouper

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--grouper', '-g', type=str, choices=['porter', 'lancaster', 'wordnet'], default='porter')
args = arg_parser.parse_args()

group = get_grouper(args)
stopwords = [line[:-1] for line in open('stopwords_frequency.txt', 'r') if len(line) > 1]
os.chdir('transcripts/processed')
transcripts = [file for file in os.listdir('.') if os.path.isfile(file)]

all_character_counts = {}
word_totals = {}
for transcript in transcripts:
    transcript_words = {}

    for character, dialogs in json.load(open(transcript, 'r', encoding='utf8')).items():
        for dialog in dialogs:
            words = [group(word) for word in nltk.word_tokenize(dialog)]
            words = [word for word in words if word not in stopwords]

            if character in transcript_words:
                words_set = transcript_words[character]
            else:
                words_set = set()
                transcript_words[character] = words_set

            for word in words:
                words_set.add(word)

    for character, words in transcript_words.items():
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

character_total_words = {character: sum(words.values()) for character, words in all_character_counts.items()}

data = (all_character_counts, word_totals, character_total_words)
json.dump(data, open('../../global_term_frequencies_doc.json', 'w', encoding='utf8'))
