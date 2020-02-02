import argparse
import json

from WordTable import WordTable
from utils import num_to_superscript

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--nwords', '-n', type=int, default=10)
args = arg_parser.parse_args()

table = WordTable(json.load(open('global_term_frequencies_log.json', 'r')))
exponent = 1.1
exponent_str = num_to_superscript(exponent)

relative_frequencies = {(character, word): table.use(character, word) ** exponent / table.word_use(word)
                        for character in table.all_charcters() for word in table.all_words()
                        if table.use(character, word) > 1.38
                        and table.use(character, word) / table.character_use(character) > 0.00016}

grouped_relative_frequencies = {}
for cw, frequency in relative_frequencies.items():
    if frequency in grouped_relative_frequencies:
        grouped_relative_frequencies[frequency].append(cw)
    else:
        grouped_relative_frequencies[frequency] = [cw]
sorted_relative_frequencies = sorted(grouped_relative_frequencies.items(), key=lambda x: -x[0])

for i in range(min(args.nwords, len(sorted_relative_frequencies))):
    frequency, cws = sorted_relative_frequencies[i]
    print(f'#{i + 1:<2} {", ".join([f"({cw[0]}, {cw[1]})" for cw in cws])} ({frequency:0.5f} : '
          f'{", ".join([f"{table.use(cw[0], cw[1]):>0.4f}{exponent_str}/{table.word_use(cw[1]):>0.4f}" for cw in cws])})')