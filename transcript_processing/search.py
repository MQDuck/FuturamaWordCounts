import json
import os

os.chdir('../transcripts/processed')
transcripts = [file for file in os.listdir('.') if os.path.isfile(file)]

target_character = "preach"

exact_matches = 0
possible_aliases = {}
for transcript in transcripts:
    character_lines = json.load(open(transcript, 'r', encoding='utf8'))
    for character in character_lines:
        if target_character in character:
            if target_character == character:
                exact_matches += 1
            elif character in possible_aliases:
                possible_aliases[character].append(transcript[:-5])
            else:
                possible_aliases[character] = [transcript[:-5]]


print(f'{target_character}: {exact_matches} episodes')
print('\n'.join([f'{alias} : {", ".join(episodes)}' for alias, episodes in possible_aliases.items()]))
