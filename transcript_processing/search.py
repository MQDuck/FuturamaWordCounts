import json
import os

os.chdir('../transcripts/processed')
transcripts = [file for file in os.listdir('.') if os.path.isfile(file)]

target_character = "colleen"

possible_aliases = set()
for transcript in transcripts:
    character_lines = json.load(open(transcript, 'r', encoding='utf8'))
    for character in character_lines:
        if target_character in character and target_character != character:
            possible_aliases.add(f'{transcript[:-5]}: {character}')

print('\n'.join(possible_aliases))
