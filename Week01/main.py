import sys
import threading
import urllib.request
import wave
from pprint import pprint

import pyaudio
import sounddevice as sd
import os
import re

from PyQt5.QtWidgets import QMessageBox, QFileDialog
from slugify import slugify
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from parsel import Selector


class Ui(QtWidgets.QMainWindow):
    def __init__(self, chunk=3024, frmat=pyaudio.paInt16, channels=2, rate=44100, py=pyaudio.PyAudio()):
        super(Ui, self).__init__()
        uic.loadUi('gui.ui', self)

        self.getContentButton = self.findChild(QtWidgets.QPushButton, 'getContentButton')
        self.recordButton = self.findChild(QtWidgets.QPushButton, 'recordButton')
        self.stopButton = self.findChild(QtWidgets.QPushButton, 'stopButton')
        self.goNextButton = self.findChild(QtWidgets.QPushButton, 'goNextButton')
        self.saveAndQuitButton = self.findChild(QtWidgets.QPushButton, 'saveAndQuitButton')

        self.urlInput = self.findChild(QtWidgets.QLineEdit, 'urlInput')
        self.textInput = self.findChild(QtWidgets.QPlainTextEdit, 'textInput')

        self.contentBrowser = self.findChild(QtWidgets.QTextBrowser, 'contentBrowser')

        self.getContentButton.clicked.connect(self.get_html_content)
        self.recordButton.clicked.connect(self.start_record)
        self.stopButton.clicked.connect(self.end_record)
        self.goNextButton.clicked.connect(self.go_next)
        self.saveAndQuitButton.clicked.connect(self.save_and_quit)

        self.CHUNK = chunk
        self.FORMAT = frmat
        self.CHANNELS = channels
        self.RATE = rate
        self.p = py
        self.frames = []
        self.st = 1
        self.stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True,
                                  frames_per_buffer=self.CHUNK)

        self.cleanR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        self.dir_path = ''
        self.current_sentence = {}
        self.sentences = []
        self.thread = None
        self.show()

    def get_html_content(self):
        url = self.urlInput.text()
        if url:
            try:
                fp = urllib.request.urlopen(url)
            except Exception as e:
                msg = QMessageBox()
                msg.setMinimumHeight(400)
                msg.setMinimumWidth(300)
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Lỗi khi lấy dữ liệu")
                msg.setInformativeText(str(e))
                msg.setWindowTitle("Lỗi khi lấy dữ liệu")
                msg.exec_()
                fp = None
            if fp:
                bytes = fp.read()
                text = bytes.decode("utf8")
                fp.close()
                sel = Selector(text=text)
                title = sel.css('title').get()
                self.dir_path = slugify(re.sub(self.cleanR, '', title))

                if not os.path.exists('./records/' + self.dir_path):
                    os.mkdir('./records/' + self.dir_path)
                with open('./records/' + self.dir_path + '/index.txt', 'w') as f:
                    f.write(url + '\n')

                result = sel.css('article').get()
                self.contentBrowser.append("""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" 
                "http://www.w3.org/TR/REC-html40/strict.dtd">\n<html><head><meta name="qrichtext" content="1" /><style 
                type="text/css">\np, li { white-space: pre-wrap; }\n</style></head><body style=" font-family:'MS Shell 
                Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;">\n<p style="-qt-paragraph-type:empty; 
                margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; 
                text-indent:0px;">""" + result + """<br /></p></body></html>""")

    def save_and_quit(self):
        try:
            print(self.sentences)
            f = open('./records/' + self.dir_path + '/index.txt', 'a', encoding='utf-8')
            for block in self.sentences:
                f.write(block['text'] + '\n')
                f.write(block['file'] + '\n')
            f.close()
            self.close()
        except Exception as e:
            print(e)

    def go_next(self):
        self.textInput.setPlainText('')

    def start_record(self):
        self.thread = threading.Thread(target=self.record)
        self.thread.setDaemon(True)
        try:
            self.thread.start()
        except (KeyboardInterrupt, SystemExit):
            sys.exit()

    def record(self):
        text = self.textInput.toPlainText()
        if text:
            print('1' if text else 'clgt')
            file_name = slugify(re.sub(self.cleanR, '', text)) + '.wav'
            self.st = 1
            self.frames = []
            stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True,
                                 frames_per_buffer=self.CHUNK)
            while True:
                data = stream.read(self.CHUNK)
                self.frames.append(data)
                print("* recording " + str(self.st))
                if not self.st:
                    break

            stream.close()

            wf = wave.open('./records/' + self.dir_path + '/' + file_name, 'wb')
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(self.frames))
            wf.close()

            self.current_sentence['text'] = text
            self.current_sentence['file'] = file_name

    def end_record(self):
        if threading.active_count() > 0:
            self.st = 0
            self.thread.join()
            self.sentences.append(self.current_sentence)
            self.current_sentence = {}
            pprint(self.sentences)

    def closeEvent(self, event):
        print(threading.active_count())


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
