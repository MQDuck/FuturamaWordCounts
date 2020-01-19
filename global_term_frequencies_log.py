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

os.chdir('transcripts')
transcripts = [file for file in os.listdir('.') if os.path.isfile(file)]
frequencies = {}
for transcript in transcripts:
    word_counts = {}
    total_words = 0

    for line in open(transcript, 'r', encoding='utf8'):
        colon = line.find(':')
        if colon != -1:
            dialog = remove_brackets(line.lower()[colon + 1:])
            words = [group(word) for word in nltk.word_tokenize(dialog)]

            for word in words:
                if word in word_counts:
                    word_counts[word] += 1
                else:
                    word_counts[word] = 1
                total_words += 1

    for word, count in word_counts.items():
        frequency = math.log(1 + count / total_words)
        if word in frequencies:
            frequencies[word] += frequency
        else:
            frequencies[word] = frequency

json.dump(frequencies, open('../global_term_frequencies_log.json', 'w'))
