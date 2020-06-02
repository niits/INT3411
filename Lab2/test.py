import os
import librosa
import math
import numpy as np
import pickle
import operator

def get_mfcc(file_path):
    y, sr = librosa.load(file_path)  # read .wav file
    hop_length = math.floor(sr*0.010)  # 10ms hop
    win_length = math.floor(sr*0.025)  # 25ms frame
    # mfcc is 12 x T matrix
    mfcc = librosa.feature.mfcc(
        y, sr, n_mfcc=12, n_fft=1024,
        hop_length=hop_length, win_length=win_length)
    # substract mean from mfcc --> normalize mfcc
    mfcc = mfcc - np.mean(mfcc, axis=1).reshape((-1, 1))
    # delta feature 1st order and 2nd order
    delta1 = librosa.feature.delta(mfcc, order=1)
    delta2 = librosa.feature.delta(mfcc, order=2)
    # X is 36 x T
    X = np.concatenate([mfcc, delta1, delta2], axis=0)  # O^r
    # return T x 36 (transpose of X)
    return X.T  # hmmlearn use T x N matrix


def get_class_data(data_dir):
    data_folder = os.path.join(data_dir)
    files = os.listdir(data_folder)
    mfcc = [get_mfcc(os.path.join(data_folder, file))
                     for file in files if file.endswith(".wav")]
    return mfcc

if __name__ == "__main__":
    class_names = ["song", "thay", "thoi_gian", "y_te", "truoc"]
    dataset_test = {}

    for name in class_names:
        folder_name = os.path.join("record", name)
        print(f"Load test {name} dataset")
        dataset_test[name] = get_class_data(folder_name)

    models = None
    with open("test.pkl", "rb") as file: 
      models = pickle.load(file)

    err = []
    for name in class_names:
        total, true_predict = 0, 0
        for item in dataset_test[name]:
            total += 1
            score = {cname: model.score(item, [len(item)]) for cname, model in models.items()}
            predict = max(score.items(), key=operator.itemgetter(1))[0]
            if predict == name:
                true_predict += 1
            else:
                err.append(f'{name}_test {total}: {len(item)}')
        if total: print(f'{name} test dataset: {math.floor(true_predict * 100 / total)} % ({true_predict} / {total})')
    with open("error.txt", "w") as file:
        for e in err:
            file.writelines(str(e) + '\n')