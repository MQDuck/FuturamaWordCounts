import argparse
import json
import os

from StemTable import StemTable
from scores import exponent, use_min, use_ratio_min
from utils import num_to_superscript

os.chdir(os.path.dirname(__file__))
stem_table = StemTable(json.load(open('stem_scores.json', 'r', encoding='utf8')))
reverse_stems = json.load(open('reverse_stems.json', 'r', encoding='utf8'))


def term_scores(character):
    aliases_single = json.load(open('aliases_single.json', 'r', encoding='utf8'))
    character = character.lower().replace('.', '')
    if character in aliases_single:
        character = aliases_single[character][0]
    elif character not in stem_table.all_characters():
        return None, None

    relative_frequencies = {stem: stem_table.use(character, stem) ** exponent / stem_table.stem_use(stem)
                            for stem in stem_table.all_stems()
                            if stem_table.use(character, stem) > use_min
                            and stem_table.use(character, stem) / stem_table.character_use(character) > use_ratio_min}

    grouped_relative_frequencies = {}
    for stem, frequency in relative_frequencies.items():
        if frequency in grouped_relative_frequencies:
            grouped_relative_frequencies[frequency].append(stem)
        else:
            grouped_relative_frequencies[frequency] = [stem]
    sorted_relative_frequencies = sorted(grouped_relative_frequencies.items(), key=lambda x: -x[0])

    return sorted_relative_frequencies, character


if __name__ == '__main__':
    def main():
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument('character', type=str)
        arg_parser.add_argument('--nterms', '-n', type=int, default=10)
        args = arg_parser.parse_args()

        character_term_scores, character = term_scores(args.character)
        if character is None:
            print(f'Unknown character: {args.character}')
            exit(1)
        character_reverse_stems = reverse_stems[character]
        exponent_str = num_to_superscript(exponent)

        for i in range(min(args.nterms, len(character_term_scores))):
            frequency, stems = character_term_scores[i]
            words = []
            scores = []
            scores_set = set()
            for stem in stems:
                words.append('/'.join(character_reverse_stems[stem]))
                score = f'{stem_table.use(character, stem):>0.4f}{exponent_str}/{stem_table.stem_use(stem):>0.4f}'
                scores.append(score)
                scores_set.add(score)
            words = ', '.join(words)
            scores = scores[0] if len(scores_set) == 1 else ', '.join(scores)
            print(f'#{i + 1:<2} {words} ({frequency:>0.5f} : {scores})')


    main()
