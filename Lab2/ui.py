import sys
import threading
import wave
import pyaudio
from PyQt5 import QtWidgets
from layout import Ui_Dialog
import librosa
import math as m
import numpy as np
import pickle
import operator


class Ui(QtWidgets.QMainWindow):
    def __init__(self, chunk=3024, frmat=pyaudio.paInt16, channels=2, rate=44100, py=pyaudio.PyAudio()):
        super(Ui, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.recordButton = self.findChild(QtWidgets.QPushButton, 'recordButton')

        self.textBrowser = self.findChild(QtWidgets.QTextBrowser, 'textBrowser')

        self.recordButton.clicked.connect(self.update)

        self.CHUNK = chunk
        self.FORMAT = frmat
        self.CHANNELS = channels
        self.RATE = rate
        self.p = py
        self.frames = []
        self.st = 0
        with open("output.pkl", "rb") as file: self.models = pickle.load(file)
        self.predict = ''
        self.thread = None
        self.show()

    def update(self):
        if self.thread and self.st:
            self.recordButton.setText('Ghi')
            self.st = 0
            self.thread.join()
            self.set_predict_text()
        else:
            self.recordButton.setText('Dung ghi')
            self.textBrowser.setText('')
            if not self.st:
                self.thread = threading.Thread(target=self.record)
                self.thread.setDaemon(True)
                try:
                    self.thread.start()
                except (KeyboardInterrupt, SystemExit):
                    sys.exit()

    def record(self):

        file_name = 'data.wav'
        self.st = 1
        self.frames = []
        stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True,
                             frames_per_buffer=self.CHUNK)
        while True:
            data = stream.read(self.CHUNK)
            self.frames.append(data)
            if not self.st:
                break

        stream.close()
        wf = wave.open(file_name, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()

        O = self.get_mfcc(file_name)
        score = {cname: model.score(O, [len(O)]) for cname, model in self.models.items()}
        self.predict = max(score.items(), key=operator.itemgetter(1))[0]
        
    def set_predict_text(self):
        text = 'Không thể đoán nhận từ vừa đọc'
        if self.predict == 'song':
            text = 'Sống'
        elif self.predict == 'thay':
            text = 'Thấy'
        elif self.predict == 'truoc':
            text = 'Trước'
        elif self.predict == 'thoi_gian':
            text = 'Thời gian'
        elif self.predict == 'y_te':
            text = 'Y tế'

        self.textBrowser.setText(text)

    def get_mfcc(self, file_path):
        y, sr = librosa.load(file_path)  # read .wav file
        hop_length = m.floor(sr * 0.010)  # 10ms hop
        win_length = m.floor(sr * 0.025)  # 25ms frame

        mfcc = librosa.feature.mfcc(
            y, sr, n_mfcc=12, n_fft=1024,
            hop_length=hop_length, win_length=win_length)

        mfcc = mfcc - np.mean(mfcc, axis=1).reshape((-1, 1))

        delta1 = librosa.feature.delta(mfcc, order=1)
        delta2 = librosa.feature.delta(mfcc, order=2)

        X = np.concatenate([mfcc, delta1, delta2], axis=0)

        return X.T


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
