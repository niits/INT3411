import os
import shutil
import sys
from pathlib import Path


sys.path.append(os.path.join(os.path.dirname(__file__), "src"))  

def create_list(files, wav_dir, exist_ok=True):
    speaker_label = os.path.basename(str(wav_dir))
    lines = []
    for wav_file_name in os.listdir(str(wav_dir)):
        if os.path.splitext(str(wav_file_name))[1] == ".wav":
            lines.append(os.path.join(str(speaker_label), os.path.splitext(str(wav_file_name))[0]))
    pos = int(len(lines) / 5 * 4)

    for use in ['train', 'eval']:
        if os.path.exists(str(files[use])):
            message = "The list file {} already exists.".format(files[use])
            if exist_ok:
                print(message)
            else:
                raise FileExistsError(message)
        else:
            split_lines = lines[:pos] if use == 'train' else lines[(pos+1):]
            print("Generate {}".format(files[use]))
            with open(str(files[use]), "w") as file_handler:
                for line in sorted(split_lines):
                    print(line, file=file_handler)


if __name__ == "__main__":
    
    LABELS = {"source": "SF3", "target":"TM3"}
    LIST_FILES = {
        'source': 
            {
                'eval': 'list/SF3_eval.list',
                'train': 'list/SF3_train.list'
            },
        'target': 
            {
            'eval': 'list/TM3_eval.list',
            'train': 'list/TM3_train.list'
            }
        }

    for part, speaker in LABELS.items():
        create_list(LIST_FILES[part], 'data/wav/' + speaker)


