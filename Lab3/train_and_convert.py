import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from src import (convert, estimate_feature_statistics, estimate_twf_and_jnt, extract_features, train_GMM)

if __name__ == "__main__":

    LABELS = {"source": "SF3", "target":"TM3"}
    LIST_FILES = {
        'source': 
            {
                'eval': os.path.join('list', 'SF3_eval.list'),
                'train': os.path.join('list', 'SF3_train.list')
            },
        'target': 
            {
                'eval': os.path.join('list', 'TM3_eval.list'),
                'train': os.path.join('list', 'TM3_train.list')
            }
        }
    
    os.makedirs(os.path.join('data', 'output'), exist_ok=True)

    print("### 1. Extract acoustic features ###")

    for speaker_part, speaker_label in LABELS.items():
            extract_features.main(
                speaker_label, 
                os.path.join('conf', 'speaker.yml'),
                str(LIST_FILES[speaker_part]['train']),
                os.path.join('data', 'wav'), 
                os.path.join('data', 'output'))

    print("### 2. Estimate acoustic feature statistics ###")

    for speaker_part, speaker_label in LABELS.items():
            estimate_feature_statistics.main(
                speaker_label, str(LIST_FILES[speaker_part]["train"]),
                os.path.join('data', 'output'))

    print("### 3. Estimate time warping function and jnt ###")
    estimate_twf_and_jnt.main(
            os.path.join('conf', 'speaker.yml'),
            os.path.join('conf', 'speaker.yml'),                    
            os.path.join('conf', 'pair.yml'),
            str(LIST_FILES["source"]["train"]),
            str(LIST_FILES["target"]["train"]),
            os.path.join('data', 'output'))

    print("### 4. Train GMM and converted GV ###")

    train_GMM.main(
            str(LIST_FILES["source"]["train"]),                    
            os.path.join('conf', 'pair.yml'),
            os.path.join('data', 'output'))

    print("### 5. Conversion based on the trained models ###")

    with open(LIST_FILES["source"]["eval"], 'r') as fp:
        for line in fp:
            f = line.rstrip()
            convert.main(
                LABELS["source"], 
                LABELS["target"],
                os.path.join('conf', 'speaker.yml'),
                os.path.join('conf', 'pair.yml'),
                os.path.join('data', 'output', 'FM'),
                os.path.join('data', 'wav', f + '.wav'),
                os.path.join('data', 'wav', f + '_out.wav'))
