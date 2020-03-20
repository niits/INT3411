# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1206, 480)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.contentBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.contentBrowser.setGeometry(QtCore.QRect(10, 60, 621, 351))
        self.contentBrowser.setObjectName("contentBrowser")
        self.urlInput = QtWidgets.QLineEdit(self.centralwidget)
        self.urlInput.setGeometry(QtCore.QRect(10, 30, 491, 20))
        self.urlInput.setObjectName("urlInput")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 91, 16))
        self.label.setObjectName("label")
        self.getContentButton = QtWidgets.QPushButton(self.centralwidget)
        self.getContentButton.setGeometry(QtCore.QRect(510, 30, 121, 23))
        self.getContentButton.setObjectName("getContentButton")
        self.recordButton = QtWidgets.QPushButton(self.centralwidget)
        self.recordButton.setGeometry(QtCore.QRect(1110, 60, 75, 31))
        self.recordButton.setObjectName("recordButton")
        self.goNextButton = QtWidgets.QPushButton(self.centralwidget)
        self.goNextButton.setGeometry(QtCore.QRect(640, 140, 101, 31))
        self.goNextButton.setObjectName("goNextButton")
        self.saveAndQuitButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveAndQuitButton.setGeometry(QtCore.QRect(650, 370, 141, 41))
        self.saveAndQuitButton.setObjectName("saveAndQuitButton")
        self.stopButton = QtWidgets.QPushButton(self.centralwidget)
        self.stopButton.setGeometry(QtCore.QRect(1110, 102, 75, 31))
        self.stopButton.setObjectName("stopButton")
        self.textInput = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.textInput.setGeometry(QtCore.QRect(640, 60, 461, 71))
        self.textInput.setPlainText("")
        self.textInput.setObjectName("textInput")
        self.statusLabel = QtWidgets.QLabel(self.centralwidget)
        self.statusLabel.setGeometry(QtCore.QRect(1110, 140, 71, 20))
        self.statusLabel.setObjectName("statusLabel")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(640, 180, 541, 91))
        self.textBrowser.setObjectName("textBrowser")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1206, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Nhập đường dẫn"))
        self.getContentButton.setText(_translate("MainWindow", "Lấy nội dung bài báo"))
        self.recordButton.setText(_translate("MainWindow", "Ghi âm"))
        self.goNextButton.setText(_translate("MainWindow", "Chuyển câu"))
        self.saveAndQuitButton.setText(_translate("MainWindow", "Lưu lại và thoát"))
        self.stopButton.setText(_translate("MainWindow", "Dừng ghi"))
        self.statusLabel.setText(_translate("MainWindow", "Đang dừng ghi"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Không có câu nào được lưu lại.</p></body></html>"))
