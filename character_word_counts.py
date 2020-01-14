#!env python3
import argparse
import os
import re

import nltk

stopwords = [line[:-1] for line in open('stopwords.txt', 'r') if len(line) > 1]

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('character', type=str)
arg_parser.add_argument('--grouper', '-g', type=str, choices=['porter', 'lancaster', 'wordnet'], default='porter')
arg_parser.add_argument('--nwords', '-n', type=int, default=10)
args = arg_parser.parse_args()

dialog_prefix = f'{args.character.lower()}: '
if args.grouper == 'porter':
    group = nltk.PorterStemmer().stem
elif args.grouper == 'lancaster':
    group = nltk.LancasterStemmer().stem
else:
    lemmatizer = nltk.WordNetLemmatizer()
    def group(s): return lemmatizer.lemmatize(s, pos='v')

os.chdir('transcripts')
transcripts = [file for file in os.listdir('.') if os.path.isfile(file)]

word_counts = {}
for transcript in transcripts:
    for line in open(transcript, 'r', encoding='utf8'):
        line = line.lower()
        prefix_loc = line.find(dialog_prefix)
        if prefix_loc != -1:
            parts = re.split('\[|\]', line[prefix_loc + len(dialog_prefix):])
            dialog = ''.join([parts[i] for i in range(len(parts)) if i % 2 == 0])
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
    print(f'{f"#{i+1}":>3} {", ".join(words)} ({count})  ')