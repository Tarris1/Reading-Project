# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 19:27:49 2018

@author: Sandsnes
"""

import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget,
                             QAction, QTableWidget,QTableWidgetItem,QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QTabWidget,
                             qApp, QInputDialog, QFileDialog, QTextEdit, QComboBox)
                             
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

class ReadingApp(QMainWindow):
    def __init__(self):
        
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        
        self.btn_progress = QPushButton('Update Progress', self) #Add Progress button
        self.btn_progress.setToolTip('Update your reading progress')
        
        self.btn_add_books = QPushButton('Add a New Book', self) ###Add a new Book button
        self.btn_add_books.setToolTip ('Add a new book to your shelf')
        #self.btn_add_books.clicked.connect (self.showDialog) #Opens up a dialog where you can "add" books
        self.btn_add_books.clicked.connect(self.addBooksFunc)
        
        self.added_book = QLabel('', self) #Label indicating added book 
        
        self.add_booksLbl = QLabel("Enter the details of a new book below:")
        #self.addNotes = QTextEdit() #
        
        self.addTitle = QLineEdit()
        self.addTitleLbl = QLabel("Title",self)
        titleHbox = QHBoxLayout()
        titleHbox.addWidget(self.addTitle)
        titleHbox.addWidget(self.addTitleLbl)
        
        self.addAuthor = QLineEdit()
        self.addAuthorLbl = QLabel("Author", self)
        AuthorHbox = QHBoxLayout()
        AuthorHbox.addWidget(self.addAuthor)
        AuthorHbox.addWidget(self.addAuthorLbl)
        
        self.addPages = QLineEdit()
        self.addPages.resize(50,20)
        self.addPagesLbl = QLabel("Pages", self)
        PagesHbox = QHBoxLayout()
        PagesHbox.addWidget(self.addPages)
        PagesHbox.addWidget(self.addPagesLbl)
        
        #Choose book to update progress on
        self.combo = QComboBox(self) 
        self.combo.addItem("Book1")
        self.combo.activated[str].connect(self.onActivated) 
        
        ProgresshBox = QHBoxLayout()
        ProgresshBox.addWidget(self.combo)
        ProgresshBox.addWidget(self.btn_progress)
        
        #####Add first tab, add books or add progress + books currently reading
        vbox = QVBoxLayout() 
        #vbox.addWidget(self.addNotes)
        vbox.addWidget(self.add_booksLbl)
        vbox.addLayout(titleHbox)
        vbox.addLayout(AuthorHbox)
        vbox.addLayout(PagesHbox)
        vbox.addWidget(self.btn_add_books)
        vbox.addWidget(self.added_book) 
        vbox.addStretch(1)
        vbox.addLayout(ProgresshBox)
        
        
        tab1 = QWidget(self) #First Tab
        self.setCentralWidget(tab1)
        tab1.setLayout(vbox)
        
        
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
            self.combo.addItem(str(text)) ###Adds another menu for added book.
            
    def openFileDialog(self): #Opens the dialog and reads the existing data in the specific file
                                #Currently only reads txt files with character limitations
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')

        if fname[0]:
            f = open(fname[0], 'r')

            with f:
                data = f.read()
                self.addNotes.setText(data)   
                
    def onActivated(self, text):
    
        self.btn_progress.setText("Update the progress of: " + text)
        
    def addBooksFunc(self):
        '''Adds book to combo widget and changes label at the bottom to indicate added book'''
        '''Also adds these details to data file ###To be added####'''
        title = self.addTitle.text()
        author = self.addAuthor.text()
        if title != "":
            if author != "":
                self.added_book.setText("You have just added " + str(title) + " by " + str(author) +
                                        " to your reading list")
                self.combo.addItem(str(title))
            else:
                self.added_book.setText("Please add the author")
        else:
            self.added_book.setText("Please add a title")
        
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ReadingApp()
    sys.exit(app.exec_())