import argparse
import json
import os

from StemTable import StemTable
from scores import exponent, use_min, use_ratio_min
from utils import num_to_superscript

os.chdir(os.path.dirname(__file__))
stem_table = StemTable(json.load(open('stem_scores.json', 'r', encoding='utf8')))
reverse_stems = json.load(open('reverse_stems.json', 'r', encoding='utf8'))


def character_scores(term):
    term = term.lower()
    if term in reverse_stems['all']:
        stem = term
        terms = reverse_stems['all'][term]
    else:
        stem = None
        terms = None
        for s, t in reverse_stems['all'].items():
            if term in t:
                stem = s
                #terms = t
                break
        if stem is None:
            return None, None

    relative_frequencies = {character: stem_table.use(character, stem) ** exponent / stem_table.stem_use(stem)
                            for character in stem_table.all_characters()
                            if stem_table.use(character, stem) > use_min
                            and stem_table.use(character, stem) / stem_table.character_use(character) > use_ratio_min}

    grouped_relative_frequencies = {}
    for character, frequency in relative_frequencies.items():
        if frequency in grouped_relative_frequencies:
            grouped_relative_frequencies[frequency].append(character)
        else:
            grouped_relative_frequencies[frequency] = [character]
    sorted_relative_frequencies = sorted(grouped_relative_frequencies.items(), key=lambda x: -x[0])

    return sorted_relative_frequencies, stem


if __name__ == '__main__':
    def main():
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument('term', type=str)
        arg_parser.add_argument('--nchars', '-n', type=int, default=10)
        args = arg_parser.parse_args()

        term_character_scores, stem = character_scores(args.term)
        if stem is None:
            print(f'Unknown term: {args.term}')
            exit(1)
        exponent_str = num_to_superscript(exponent)

        for i in range(min(args.nchars, len(term_character_scores))):
            frequency, characters = term_character_scores[i]
            score = f'{stem_table.use(characters[0], stem):>0.4f}{exponent_str}/{stem_table.stem_use(stem):>0.4f}'
            characters = ', '.join([f'{character} ({", ".join(reverse_stems[character][stem])})' for character in characters])
            print(f'#{i + 1:<2} {characters} ({frequency:>0.5f} : {score})')

    main()
