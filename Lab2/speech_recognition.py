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


def get_class_data(data_dir):
    files = os.listdir(data_dir)
    mfcc = [get_mfcc(os.path.join(data_dir, f))
                     for f in files if f.endswith(".wav")]
    return mfcc


def clustering(X, n_clusters=10):
    kmeans = KMeans(n_clusters=n_clusters, n_init=50,
                    random_state=0, verbose=0)
    kmeans.fit(X)
    print("centers", kmeans.cluster_centers_.shape)
    return kmeans


if __name__ == "__main__":
    class_names = ["song", "thay", "test_song", "test_thay", "thoi_gian",  "test_thoi_gian", "y_te", "test_y_te", "truoc", "test_truoc"]
    dataset = {}
    for cname in class_names:
        print(f"Load {cname} dataset")
        dataset[cname] = get_class_data(os.path.join("data", cname))

    models = {}
    for cname in class_names:

        hmm = hmmlearn.hmm.GMMHMM(
            n_components=5, n_mix=2, random_state=42, n_iter=1000, verbose=True,
            params='mctw',
            init_params='mc',
            #         startprob_prior = np.array([1.0,0.0,0.0,0.0,0.0]),
            #         transmat_prior = np.array([
            #             [0.7,0.3,0.0,0.0,0.0],
            #             [0.0,0.7,0.3,0.0,0.0],
            #             [0.0,0.0,0.7,0.3,0.0],
            #             [0.0,0.0,0.0,0.7,0.3],
            #             [0.0,0.0,0.0,0.0,1.0],
            #         ])
        )
        hmm.startprob_ = np.array([1.0, 0.0, 0.0, 0.0, 0.0])
    #     hmm.transmat_ = np.array([
    #             [0.7,0.3,0.0,0.0,0.0],
    #             [0.0,0.7,0.3,0.0,0.0],
    #             [0.0,0.0,0.7,0.3,0.0],
    #             [0.0,0.0,0.0,0.7,0.3],
    #             [0.0,0.0,0.0,0.0,1.0],
    #         ])
    #     hmm.transmat_ += 1e-2
    #     hmm.transmat_ = hmm.transmat_ / np.sum(hmm.transmat_, axis=1)
        if cname[:4] != 'test':
            X = np.concatenate(dataset[cname])
            lengths = list([len(x) for x in dataset[cname]])
            print("training class", cname)
            print(X.shape, lengths, len(lengths))
            hmm.fit(X)
            models[cname] = hmm

    print("Training done")

    with open("output.pkl", "wb") as file:
        pickle.dump(models, file)

    print("Testing")
    for true_cname in class_names:
        total = 0
        true_predict = 0
        for O in dataset[true_cname]:
            total = total + 1
            score = {cname: model.score(O, [len(O)]) for cname, model in models.items() if cname[:4] != 'test'}
            predict = max(score.items(), key=operator.itemgetter(1))[0]
            true_predict = true_predict + int(predict == (true_cname[5:] if true_cname[:4] == 'test' else true_cname))
        print(true_cname, math.floor(true_predict * 100 / total), '%')

