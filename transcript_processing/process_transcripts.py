import json
import os
import re


def remove_brackets(s):
    parts = re.split('\[|\]', s)
    s = ''.join([parts[i] for i in range(len(parts)) if i % 2 == 0])
    parts = re.split('\(|\)', s)
    s = ''.join([parts[i] for i in range(len(parts)) if i % 2 == 0])
    parts = re.split('<|>', s)
    return ''.join([parts[i] for i in range(len(parts)) if i % 2 == 0])


# noinspection PyShadowingNames
def add_line(character, dialog, character_lines):
    if character in character_lines:
        character_lines[character].append(dialog)
    else:
        character_lines[character] = [dialog]


aliases_single = json.load(open('aliases_single.json', 'r', encoding='utf8'))
aliases_multiple = json.load(open('aliases_multiple.json', 'r', encoding='utf8'))
aliases_cornwood = json.load(open('aliases_cornwood.json', 'r', encoding='utf8'))
aliases = {**aliases_single, **aliases_cornwood}
os.chdir('../transcripts')
transcripts = [file for file in os.listdir('unprocessed') if os.path.isfile(f'unprocessed/{file}')]
if not os.path.exists('processed'):
    os.mkdir('processed')

for transcript in transcripts:
    character_lines = {}

    for line in open(f'unprocessed/{transcript}', 'r', encoding='utf8'):
        line = remove_brackets(line)
        colon = line.find(':')
        if colon != -1:
            character = line[:colon].lower().strip()
            if 'farnsoworth' in character:
                print(line)
            dialog = line[colon + 1:].lower()
            if character in aliases:
                for alias in aliases[character]:
                    add_line(alias, dialog, character_lines)
            else:
                add_line(character, dialog, character_lines)

    json.dump(character_lines, open(f'processed/{".".join(transcript.split(".")[:-1])}.json', 'w', encoding='utf8'))
