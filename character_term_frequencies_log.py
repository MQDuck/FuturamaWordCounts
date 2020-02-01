import argparse
import json

from WordTable import WordTable
from utils import num_to_superscript

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('character', type=str)
arg_parser.add_argument('--nwords', '-n', type=int, default=10)
args = arg_parser.parse_args()

table = WordTable(json.load(open('global_term_frequencies_log.json', 'r')))
character = args.character.lower()
exponent = 1.4
exponent_str = num_to_superscript(exponent)


def score(word):
    usage = table.use(character, word)
    # character_total = word_table.character_use(character)
    word_total = table.word_use(word)
    return usage ** exponent / word_total


if character not in table.all_charcters():
    print(f'Unknown character: {args.character}')
    exit(1)

relative_frequencies = {word: score(word) for word in table.all_words()
                        if table.use(character, word) > 1.38
                        and table.use(character, word) / table.character_use(character) > 0.0002}

grouped_relative_frequencies = {}
for word, frequency in relative_frequencies.items():
    if frequency in grouped_relative_frequencies:
        grouped_relative_frequencies[frequency].append(word)
    else:
        grouped_relative_frequencies[frequency] = [word]
sorted_relative_frequencies = sorted(grouped_relative_frequencies.items(), key=lambda x: -x[0])

for i in range(min(args.nwords, len(sorted_relative_frequencies))):
    frequency, words = sorted_relative_frequencies[i]
    print(f'#{i + 1:<2} {", ".join(words)} ({frequency:0.5f} : '
          f'{", ".join([f"{table.use(character, word):>0.4f}{exponent_str}/{table.word_use(word):>0.4f}" for word in words])})')
