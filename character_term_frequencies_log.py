import argparse
import json

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('character', type=str)
arg_parser.add_argument('--grouper', '-g', type=str, choices=['porter', 'lancaster', 'wordnet'], default='porter')
arg_parser.add_argument('--nwords', '-n', type=int, default=10)
args = arg_parser.parse_args()

all_character_sums, word_totals, character_total_sums = \
    tuple(json.load(open('global_term_frequencies_log.json', 'r')))
character = args.character.lower()
exponent = 1.4
exponent_str = ''.join([{'0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸',
                         '9': '⁹', '+': '⁺', '-': '⁻', '.': '⋅'}[d] for d in str(exponent)])

if character not in all_character_sums:
    print(f'Unknown character: {args.character}')
    exit(1)

word_sums = all_character_sums[character]
total_sum = character_total_sums[character]

relative_frequencies = {word: word_sum ** exponent / word_totals[word] for word, word_sum in word_sums.items()
                        if word_sum > 1.38 and word_sum / total_sum > 0.0002}

grouped_relative_frequencies = {}
for word, frequency in relative_frequencies.items():
    if frequency in grouped_relative_frequencies:
        grouped_relative_frequencies[frequency].append(word)
    else:
        grouped_relative_frequencies[frequency] = [word]
sorted_relative_frequencies = sorted(grouped_relative_frequencies.items(), key=lambda x: -x[0])

for i in range(min(20, len(sorted_relative_frequencies))):
    frequency, words = sorted_relative_frequencies[i]
    print(f'#{i + 1:<2} {", ".join(words)} ({frequency:0.5f} : '
          f'{", ".join([f"{word_sums[word]:>0.4f}{exponent_str}/{word_totals[word]:>0.4f}" for word in words])})')
