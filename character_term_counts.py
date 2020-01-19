#!env python3
import argparse
import os
import re

import nltk

from utils import remove_brackets, get_grouper

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('character', type=str)
arg_parser.add_argument('--grouper', '-g', type=str, choices=['porter', 'lancaster', 'wordnet'], default='porter')
arg_parser.add_argument('--nwords', '-n', type=int, default=10)
args = arg_parser.parse_args()

dialog_prefix = f'{args.character.lower()}: '
group = get_grouper(args)
stopwords = [line[:-1] for line in open('stopwords.txt', 'r') if len(line) > 1]

os.chdir('transcripts')
transcripts = [file for file in os.listdir('.') if os.path.isfile(file)]
word_counts = {}
for transcript in transcripts:
    for line in open(transcript, 'r', encoding='utf8'):
        line = line.lower()
        prefix_loc = line.find(dialog_prefix)
        if prefix_loc != -1:
            dialog = remove_brackets(line[prefix_loc + len(dialog_prefix):])
            words = [group(word) for word in nltk.word_tokenize(dialog) if word not in stopwords]
            words = [word for word in words if word not in stopwords]

            for word in words:
                if word in word_counts:
                    word_counts[word] += 1
                else:
                    word_counts[word] = 1

grouped_word_counts = {}
for word, count in word_counts.items():
    if count in grouped_word_counts:
        grouped_word_counts[count].append(word)
    else:
        grouped_word_counts[count] = [word]

sorted_words = sorted(grouped_word_counts.items(), key=lambda x: -x[0])
print(f'**{args.character}**  ')
for i, (count, words) in enumerate(sorted_words[:args.nwords]):
    place = f'\\#{i+1}'
    print(f'{place:>3} {", ".join(words)} ({count})  ')
    #print(f'{f"#{i+1}":>3} {", ".join(words)} ({count})  ')

# print()
# top = [group(word) for word in
#        ['meatbag']]
# for i, (count, words) in enumerate(sorted_words):
#     for word in words:
#         if word in top:
#             print(f'{word} (#{i+1})  ')
# print(word_counts['meatbag'])