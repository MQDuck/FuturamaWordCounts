import json
import os

from utils import split_line


def add_possible_alias(target_character, possible_alias, transcript):
    episode = transcript[:-4]
    if possible_alias == target_character:
        exact_matches.add(episode)
    elif possible_alias in possible_aliases:
        possible_aliases[possible_alias].add(episode)
    else:
        possible_aliases[possible_alias] = {episode}


aliases_single = json.load(open('../aliases_single.json', 'r', encoding='utf8'))
aliases_multiple = json.load(open('../aliases_multiple.json', 'r', encoding='utf8'))
aliases_cornwood = json.load(open('../aliases_cornwood.json', 'r', encoding='utf8'))
aliases = {**aliases_single, **aliases_cornwood, **aliases_multiple}
os.chdir('../transcripts')
transcripts = [file for file in os.listdir('../transcripts') if os.path.isfile(file)]

target_character = "god".lower().replace('.', '')

exact_matches = set()
possible_aliases = {}
for transcript in transcripts:
    for line in open(transcript, 'r', encoding='utf8'):
        character, _ = split_line(line)
        if len(character) != 0 and target_character in character:
            if character in aliases:
                for alias in aliases[character]:
                    if target_character in alias:
                        add_possible_alias(target_character, alias, transcript)
            else:
                add_possible_alias(target_character, character, transcript)

print(f'{target_character} : {", ".join(exact_matches)}')
print('\n'.join([f'{alias} : {", ".join(episodes)}' for alias, episodes in possible_aliases.items()]))
