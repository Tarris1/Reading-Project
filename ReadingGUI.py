# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 19:27:49 2018

@author: Sandsnes
"""

import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget,
                             QAction, QTableWidget,QTableWidgetItem,QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, 
                             qApp, QInputDialog, QFileDialog, QTextEdit)
                             
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

class ReadingApp(QMainWindow):
    def __init__(self):
        
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        
        btn_progress = QPushButton('Update Progress', self) 
        btn_progress.setToolTip('Update your reading progress')
        btn_add_books = QPushButton('Add a New Book', self)
        btn_add_books.setToolTip ('Add a new book to your shelf')
        btn_add_books.clicked.connect (self.showDialog) #Opens up a dialog where you can "add" books
        
        self.added_book = QLabel('', self)
        
        self.addNotes = QTextEdit() #
        
        hbox = QHBoxLayout()
        hbox.addWidget(btn_progress)
        hbox.addWidget(btn_add_books)
        
        vbox = QVBoxLayout() 
        vbox.addWidget(self.addNotes)
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addWidget(self.added_book) #Is aded below the horizontal book
        
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
        
        openFile = QAction(QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.openFileDialog)
        
        self.statusBar()
        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)
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
    
    
    def showDialog(self): #Dialog function 
        
        text, ok = QInputDialog.getText(self, 'Input Dialog',  #Dialog title, Dialog message
            'Enter a new Book Title:') #Returns text and a boolean value (TRUE or FALSE)
        
        if ok:
            self.added_book.setText("You have just added " + str(text) + " to your reading list") 
            #Sets text of QLabel
            
    def openFileDialog(self): #Opens the dialog and reads the existing data in the specific file
                                #Currently only reads txt files with character limitations
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')

        if fname[0]:
            f = open(fname[0], 'r')

            with f:
                data = f.read()
                self.addNotes.setText(data)   
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ReadingApp()
    sys.exit(app.exec_())