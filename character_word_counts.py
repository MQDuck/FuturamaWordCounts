#!env python3
import argparse
import json
import os
import re

import nltk

stopwords = [line[:-1] for line in open('stopwords.txt', 'r') if len(line) > 1]
lemmatizer = nltk.WordNetLemmatizer()

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('character', type=str)
args = arg_parser.parse_args()

character = f'{args.character.lower()}: '

lemma_counts = {}
os.chdir('transcripts')
transcripts = [file for file in os.listdir('.') if
               os.path.isfile(file)]
for transcript in transcripts:
    for line in open(transcript, 'r', encoding='utf8'):
        line = line.lower()
        if line.startswith(character):
            parts = re.split('\[|\]', line[len(character):])
            line_speech = ''.join([parts[i] for i in range(len(parts)) if i % 2 == 0])
            tokens = [word for word in nltk.word_tokenize(line_speech) if word not in stopwords]
            lemmas = [lemmatizer.lemmatize(token, pos='v') for token in tokens]
            lemmas = [lemma for lemma in lemmas if lemma not in stopwords]

            for lemma in lemmas:
                if lemma in lemma_counts:
                    lemma_counts[lemma] += 1
                else:
                    lemma_counts[lemma] = 1

sorted_lemmas = sorted(lemma_counts.items(), key=lambda x: -x[1])
for lemma, count in sorted_lemmas[:20]:
    print(f'{lemma:10} {count:>4}')
