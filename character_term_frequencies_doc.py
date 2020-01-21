import argparse
import json

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('character', type=str)
arg_parser.add_argument('--grouper', '-g', type=str, choices=['porter', 'lancaster', 'wordnet'], default='porter')
arg_parser.add_argument('--nwords', '-n', type=int, default=10)
args = arg_parser.parse_args()

all_character_counts, word_totals, character_total_words = \
    tuple(json.load(open('global_term_frequencies_doc.json', 'r')))
character = args.character.lower()

if character not in all_character_counts:
    print(f'Unknown character: {args.character}')
    exit(1)

word_counts = all_character_counts[character]
total_words = character_total_words[character]
relative_frequencies = {word: count ** 1.2 / word_totals[word] for word, count in word_counts.items()
                        if count > 2 and count / total_words > 0.0002}

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
          f'{", ".join([f"{word_counts[word]}/{word_totals[word]}" for word in words])})')
