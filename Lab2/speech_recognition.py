import librosa
import numpy as np
import os
import math
from sklearn.cluster import KMeans
import hmmlearn.hmm
import operator
import pickle
from pprint import pprint


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


def get_class_data(data_dir, target):
    data_folder = os.path.join(data_dir, target)
    files = os.listdir(data_folder)
    mfcc = [get_mfcc(os.path.join(data_folder, file))
                     for file in files if file.endswith(".wav")]
    return mfcc


if __name__ == "__main__":
    class_names = ["song", "thay", "thoi_gian", "y_te", "truoc"]
    dataset_train, dataset_test = {}, {}

    for name in class_names:
        folder_name = os.path.join("data", name)
        print(f'{name}:')
        print(' - Load train dataset')
        dataset_train[name] = get_class_data(folder_name, 'train')
        print(" - Load test dataset")
        dataset_test[name] = get_class_data(folder_name, 'test')

    models = {}
    for name in class_names:
        hmm = hmmlearn.hmm.GMMHMM(
            n_mix=2, random_state=42, n_iter=1000, verbose=False,
            params='mctw',
            init_params='mct'    
        )
        if name == 'song':
            hmm.n_components = 6
            hmm.startprob_ = np.array([0.8, 0.2, 0.0, 0.0, 0.0, 0.0])
            hmm.transmat_ = np.array([
                        [0.7,0.3,0.0,0.0,0.0,0.0],
                        [0.0,0.7,0.3,0.0,0.0,0.0],
                        [0.0,0.0,0.7,0.3,0.0,0.0],
                        [0.0,0.0,0.0,1.0,0.0,0.0],
                        [0.0,0.0,0.0,0.0,0.7,0.3],
                        [0.0,0.0,0.0,0.0,0.0,1.0],
                    ])
        elif name == 'truoc':
            hmm.n_components = 6
            hmm.startprob_ = np.array([0.8, 0.2, 0.0, 0.0, 0.0, 0.0])
            hmm.transmat_ = np.array([
                        [0.7,0.3,0.0,0.0,0.0,0.0],
                        [0.0,0.7,0.3,0.0,0.0,0.0],
                        [0.0,0.0,0.7,0.3,0.0,0.0],
                        [0.0,0.0,0.0,1.0,0.0,0.0],
                        [0.0,0.0,0.0,0.0,0.7,0.3],
                        [0.0,0.0,0.0,0.0,0.0,1.0],
                    ])
        elif name == 'thay':
            hmm.n_components = 5
            hmm.startprob_ = np.array([1.0, 0.0, 0.0, 0.0, 0.0])
            hmm.transmat_ = np.array([
                        [0.7,0.3,0.0,0.0,0.0],
                        [0.0,0.7,0.3,0.0,0.0],
                        [0.0,0.0,0.7,0.3,0.0],
                        [0.0,0.0,0.0,0.7,0.3],
                        [0.0,0.0,0.0,0.0,1.0],
                    ])
        
        elif name == 'thoi_gian':
            hmm.n_components = 12
            hmm.startprob_ = np.array([1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
            hmm.transmat_ = np.array([
                        [0.7,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],
                        [0.0,0.7,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],
                        [0.0,0.0,0.7,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],
                        [0.0,0.0,0.0,0.7,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.0],
                        [0.0,0.0,0.0,0.0,0.7,0.3,0.0,0.0,0.0,0.0,0.0,0.0],
                        [0.0,0.0,0.0,0.0,0.0,0.7,0.3,0.0,0.0,0.0,0.0,0.0],
                        [0.0,0.0,0.0,0.0,0.0,0.0,0.7,0.3,0.0,0.0,0.0,0.0],
                        [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.7,0.3,0.0,0.0,0.0],
                        [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.7,0.3,0.0,0.0],
                        [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.7,0.3,0.0],
                        [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.7,0.3],
                        [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0],
                    ])
        elif name == 'y_te':
            hmm.n_components = 5
            hmm.startprob_ = np.array([0.8, 0.2, 0.0, 0.0, 0.0])
            hmm.transmat_ = np.array([
                        [0.7,0.3,0.0,0.0,0.0],
                        [0.0,0.7,0.3,0.0,0.0],
                        [0.0,0.0,0.7,0.3,0.0],
                        [0.0,0.0,0.0,0.7,0.3],
                        [0.0,0.0,0.0,0.0,1.0],
                    ])
        X = np.concatenate(dataset_train[name])
        lengths = list([len(x) for x in dataset_train[name]])
        print("Training class", name)
        print(X.shape, lengths, len(lengths))
        hmm.fit(X)
        models[name] = hmm

    print("Training done!")

    with open("output_huy.pkl", "wb") as file:
        pickle.dump(models, file)

    print("Testing...")
    err = []
    for name in class_names:
        total, true_predict = 0, 0
        for item in dataset_train[name]:
            total += 1
            score = {cname: model.score(item, [len(item)]) for cname, model in models.items()}
            predict = max(score.items(), key=operator.itemgetter(1))[0]
            if predict == name:
                true_predict += 1
            else:
                err.append(f'{name}_train {total}: {len(item)}')
        print(f'{name} train dataset: {math.floor(true_predict * 100 / total)} % ({true_predict} / {total})')
        total, true_predict = 0, 0
        for item in dataset_test[name]:
            total += 1
            score = {cname: model.score(item, [len(item)]) for cname, model in models.items()}
            predict = max(score.items(), key=operator.itemgetter(1))[0]
            if predict == name:
                true_predict += 1
            else:
                err.append(f'{name}_test {total}: {len(item)}')
        print(f'{name} test dataset: {math.floor(true_predict * 100 / total)} % ({true_predict} / {total})')
    with open("error.txt", "w") as file:
        for e in err:
            file.writelines(str(e) + '\n')