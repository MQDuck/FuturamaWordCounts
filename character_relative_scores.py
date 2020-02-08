import argparse
import json

from StemTable import StemTable
from utils import num_to_superscript

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('character', type=str)
arg_parser.add_argument('--nwords', '-n', type=int, default=10)
args = arg_parser.parse_args()

table = StemTable(json.load(open('stem_scores.json', 'r')))
aliases_single = json.load(open('aliases_single.json', 'r', encoding='utf8'))
character = args.character.lower().replace('.', '')
if character in aliases_single:
    character = aliases_single[character][0]
elif character not in table.all_characters():
    print(f'Unknown character: {args.character}')
    exit(1)
reverse_stems = json.load(open('reverse_stems.json', 'r', encoding='utf8'))[character]
exponent = 1.4
exponent_str = num_to_superscript(exponent)

relative_frequencies = {stem: table.use(character, stem) ** exponent / table.stem_use(stem)
                        for stem in table.all_stems()
                        if table.use(character, stem) > 1.38
                        and table.use(character, stem) / table.character_use(character) > 0.00016}

grouped_relative_frequencies = {}
for stem, frequency in relative_frequencies.items():
    if frequency in grouped_relative_frequencies:
        grouped_relative_frequencies[frequency].append(stem)
    else:
        grouped_relative_frequencies[frequency] = [stem]
sorted_relative_frequencies = sorted(grouped_relative_frequencies.items(), key=lambda x: -x[0])

for i in range(min(args.nwords, len(sorted_relative_frequencies))):
    frequency, stems = sorted_relative_frequencies[i]
    words = ', '.join(['/'.join(reverse_stems[stem]) for stem in stems])
    scores = ', '.join([f'{table.use(character, stem):>0.4f}{exponent_str}/{table.stem_use(stem):>0.4f}'
                        for stem in stems])
    print(f'#{i + 1:<2} {words} ({frequency:>0.5f} : {scores})')
