import os
import sys
from pprint import pprint

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from src import (convert, estimate_feature_statistics, estimate_twf_and_jnt, extract_features, train_GMM)

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

    
    os.makedirs('data/output', exist_ok=True)

    print("### 1. Extract acoustic features ###")

    for speaker_part, speaker_label in LABELS.items():
            extract_features.main(
                speaker_label, "conf/speaker.yml",
                str(LIST_FILES[speaker_part]['train']),
                'data/wav', 'data/output')

    print("### 2. Estimate acoustic feature statistics ###")

    for speaker_part, speaker_label in LABELS.items():
            estimate_feature_statistics.main(
                speaker_label, str(LIST_FILES[speaker_part]["train"]),
                'data/output')

    print("### 3. Estimate time warping function and jnt ###")
    estimate_twf_and_jnt.main(
            "conf/speaker.yml",
            "conf/speaker.yml",
            str("conf/pair.yml"),
            str(LIST_FILES["source"]["train"]),
            str(LIST_FILES["target"]["train"]),
            'data/output')

    print("### 4. Train GMM and converted GV ###")

    train_GMM.main(
            str(LIST_FILES["source"]["train"]),
            str("conf/pair.yml"),
            'data/output')

    print("### 5. Conversion based on the trained models ###")
    EVAL_LIST_FILE = LIST_FILES["source"]["eval"]
    print(EVAL_LIST_FILE)
    convert.main(
            LABELS["source"], LABELS["target"],
            "conf/speaker.yml",
            str("conf/pair.yml"),
            str(EVAL_LIST_FILE),
            'data/wav',
            'data/output')
    convert.main(
            "-gmmmode", "diff",
            LABELS["source"], LABELS["target"],
            "conf/speaker.yml",
            str("conf/pair.yml"),
            str(EVAL_LIST_FILE),
            'data/wav',
            'data/output')