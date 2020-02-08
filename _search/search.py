import os

from utils import split_line

os.chdir('../transcripts')
transcripts = [file for file in os.listdir('../transcripts') if os.path.isfile(file)]

for transcript in transcripts:
    for line in open(transcript, 'r', encoding='utf8'):
        character, dialog = split_line(line)
        if len(character) != 0 and 'brain' in dialog:
            print(f'{character}: {dialog}')
