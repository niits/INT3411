import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from src import (convert)

if __name__ == "__main__":
    convert.main(
            'SF3', 
            'TF3',
            os.path.join('conf', 'speaker.yml'),
            os.path.join('conf', 'pair.yml'),
            os.path.join('data', 'output', 'FF'),
            os.path.join('data', 'wav','TF3', '001.wav'),
            'D:/a.wav')
