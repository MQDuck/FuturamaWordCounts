import argparse
import json
import math
import os

import nltk

from utils import get_grouper, remove_brackets

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('character', type=str)
arg_parser.add_argument('--grouper', '-g', type=str, choices=['porter', 'lancaster', 'wordnet'], default='porter')
arg_parser.add_argument('--nwords', '-n', type=int, default=10)
args = arg_parser.parse_args()

dialog_prefix = f'{args.character.lower()}: '
group = get_grouper(args)
global_frequencies = json.load(open('global_term_frequencies_log.json', 'r'))
stopwords = [line[:-1] for line in open('stopwords_doc.txt', 'r') if len(line) > 1]

os.chdir('transcripts')
transcripts = [file for file in os.listdir('.') if os.path.isfile(file)]
frequencies = {}
word_counts = {}
word_total = 0
for transcript in transcripts:
    transcript_word_counts = {}
    script_word_total = 0

    for line in open(transcript, 'r', encoding='utf8'):
        line = line.lower()
        prefix_loc = line.find(dialog_prefix)
        if prefix_loc != -1:
            dialog = remove_brackets(line[prefix_loc + len(dialog_prefix):])
            words = [group(word) for word in nltk.word_tokenize(dialog)]
            words = [word for word in words if word not in stopwords]

            for word in words:
                if word in transcript_word_counts:
                    transcript_word_counts[word] += 1
                else:
                    transcript_word_counts[word] = 1
                script_word_total += 1

                if word in word_counts:
                    word_counts[word] += 1
                else:
                    word_counts[word] = 1
                word_total += 1

        for word, count in transcript_word_counts.items():
            frequency = math.log(1 + count / script_word_total)
            if word in frequencies:
                frequencies[word] += frequency
            else:
                frequencies[word] = frequency

relative_frequencies = {word: frequency / global_frequencies[word] for word, frequency in frequencies.items() if
                        word_counts[word] / word_total > 0.00025}
sorted_relative_frequencies = sorted(relative_frequencies.items(), key=lambda x: -x[1])

for i in range(min(20, len(sorted_relative_frequencies))):
    word, frequency = sorted_relative_frequencies[i]
    print(f'#{i+1:<2} {word} ({frequency:0.5f})')
