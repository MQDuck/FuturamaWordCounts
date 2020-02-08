import json
import os

from utils import split_line

aliases_single = json.load(open('../aliases_single.json', 'r', encoding='utf8'))
aliases_multiple = json.load(open('../aliases_multiple.json', 'r', encoding='utf8'))
aliases_cornwood = json.load(open('../aliases_cornwood.json', 'r', encoding='utf8'))
aliases = {**aliases_single, **aliases_cornwood, **aliases_multiple}
os.chdir('../transcripts')
transcripts = [file for file in os.listdir('../transcripts') if os.path.isfile(file)]

for transcript in transcripts:
    for line in open(transcript, 'r', encoding='utf8'):
        if 'give me that robot brain' in line:
            print('foo')
        character, dialog = split_line(line)
        if len(character) > 30:
            print(f'{transcript[:-4]} : {character}')
        elif len(character) == 0 and len(dialog) != 0:
            print(f'{transcript[:-4]} : {dialog}')
