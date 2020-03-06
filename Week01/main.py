import sys
import urllib.request
import sounddevice as sd
import os
import re

from PyQt5.QtWidgets import QMessageBox
from slugify import slugify
from PyQt5 import QtWidgets, uic
from parsel import Selector


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('gui.ui', self)
        self.recording = False
        self.fs = 44100
        self.getContentButton = self.findChild(QtWidgets.QPushButton, 'getContentButton')
        self.recordButton = self.findChild(QtWidgets.QPushButton, 'recordButton')
        self.goPrevButton = self.findChild(QtWidgets.QPushButton, 'goPrevButton')
        self.goNextButton = self.findChild(QtWidgets.QPushButton, 'goNextButton')
        self.saveAndQuitButton = self.findChild(QtWidgets.QPushButton, 'saveAndQuitButton')

        self.urlInput = self.findChild(QtWidgets.QLineEdit, 'urlInput')

        self.contentBrowser = self.findChild(QtWidgets.QTextBrowser, 'contentBrowser')
        self.currentSentenceBrowser = self.findChild(QtWidgets.QTextBrowser, 'currentSentenceBrowser')

        self.getContentButton.clicked.connect(self.get_html_content)
        self.recordButton.clicked.connect(self.on_record_button_click)
        self.goNextButton.clicked.connect(self.go_next)
        self.goPrevButton.clicked.connect(self.go_prev)
        self.saveAndQuitButton.clicked.connect(self.save_and_quit)

        self.cleanR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        self.dir = ''
        self.sentences = []
        self.currentIndex = 0
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
                self.dir = slugify(re.sub(self.cleanR, '', title))
                if not os.path.exists('./records/' + self.dir):
                    os.mkdir('./records/' + self.dir)
                with open('./records/' + self.dir + '/index.txt', 'w') as f:
                    f.write(url + '\n')
                result = sel.css('article').get()
                self.contentBrowser.append("""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" 
                "http://www.w3.org/TR/REC-html40/strict.dtd">\n<html><head><meta name="qrichtext" content="1" /><style 
                type="text/css">\np, li { white-space: pre-wrap; }\n</style></head><body style=" font-family:'MS Shell 
                Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;">\n<p style="-qt-paragraph-type:empty; 
                margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; 
                text-indent:0px;">""" + result + """<br /></p></body></html>""")
                cleantext = re.sub(self.cleanR, '', result)
                cleantext = re.sub(r"[\n\t\xa0]*", '', cleantext)
                sentences = cleantext.split('.')
                self.sentences = [{'text': element, 'file': ''} for element in sentences]
                self.currentSentenceBrowser.setText(self.sentences[self.currentIndex]['text'])

    def go_next(self):
        self.currentIndex = (self.currentIndex + 1) % len(self.sentences)
        self.currentSentenceBrowser.setText(self.sentences[self.currentIndex]['text'])

    def go_prev(self):
        self.currentIndex = (self.currentIndex - 1 + len(self.sentences)) % len(self.sentences)
        self.currentSentenceBrowser.setText(self.sentences[self.currentIndex]['text'])

    def on_record_button_click(self):
        if self.recording:
            self.recordButton.setText('Ghi')
            self.recording = False
            self.end_record()
        else:
            self.recordButton.setText('Dừng Ghi')
            self.recording = True
            self.start_record()

    def save_and_quit(self):
        f = open('./records/' + self.dir + '/index.txt', 'a', encoding='utf-8')
        for block in self.sentences:
            f.write(block['text'] + '\n')
            f.write(block['file'] + '\n')
        f.close()
        self.close()
    def start_record(self):
        print(self.currentIndex + 'start_record')

    def end_record(self):
        print(self.currentIndex + 'end_record')


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
