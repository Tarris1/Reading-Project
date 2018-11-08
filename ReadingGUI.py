# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 19:27:49 2018

@author: Sandsnes
"""

import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget,
                             QAction, QTableWidget,QTableWidgetItem,QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, qApp)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

class ReadingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        
        btn_progress = QPushButton('Update Progress', self)
        btn_progress.setToolTip('Update your reading progress')
        btn_progress.resize(btn_progress.sizeHint())
        btn_add_books = QPushButton('Add a New Book', self)
        btn_add_books.setToolTip ('Add a new book to your shelf')
        btn_add_books.resize(btn_add_books.sizeHint())
        
        
        hbox = QHBoxLayout()
        hbox.addWidget(btn_progress)
        hbox.addWidget(btn_add_books)
        
        
        vbox = QVBoxLayout() 
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        
        wid = QWidget(self)
        self.setCentralWidget(wid)
        wid.setLayout(vbox)
        
        exitAct = QAction(QIcon('exit24.png'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q') #Short cut for exiting app
        exitAct.setStatusTip('Exit application') #When hovering over exit option, show message
        exitAct.triggered.connect(qApp.quit) #Adds the function to the menu option
        
        saveFile = QAction(QIcon('save.png'), '&Save', self)
        saveFile.setShortcut('Ctrl+S')
        saveFile.setStatusTip('Save your data')
        
        self.statusBar()
        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(saveFile)
        fileMenu.addAction(exitAct)
        
        # Show widget
        self.setWindowIcon(QIcon('readinglogo.jpg'))
        
        self.left = 50
        self.top = 100
        self.width = 1000
        self.height = self.width
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle("Reading & Me")
        
        self.show()
    
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ReadingApp()
    sys.exit(app.exec_())