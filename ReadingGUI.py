# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 19:27:49 2018

@author: Sandsnes
"""

import sys
import csv
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget,
                             QAction, QTableWidget,QTableWidgetItem,QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QTabWidget,
                             qApp, QInputDialog, QFileDialog, QTextEdit, QComboBox)
                             
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QDateTime

class ReadingApp(QMainWindow):
    def __init__(self):
        
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        
        self.bookShelf = [] #Ensure that a bookShelf exists
        self.updates = []
        
        ##################Widgets##################
        self.btn_progress = QPushButton('Update Progress', self) #Add Progress button
        self.btn_progress.setToolTip('Update your reading progress')
        self.btn_progress.clicked.connect(self.addProgress)
        
        self.btn_add_books = QPushButton('Add a New Book', self) ###Add a new Book button
        self.btn_add_books.setToolTip ('Add a new book to your shelf')
        #self.btn_add_books.clicked.connect (self.showDialog) #Opens up a dialog where you can "add" books
        self.btn_add_books.clicked.connect(self.addBooksFunc)
        
        self.added_book = QLabel('', self) #Label indicating added book 
        
        self.add_booksLbl = QLabel("Enter the details of a new book below:")
        #self.addNotes = QTextEdit() #
        
        #Entry lines and labels
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
        self.addPagesLbl = QLabel("Pages", self)
        PagesHbox = QHBoxLayout()
        PagesHbox.addWidget(self.addPages)
        PagesHbox.addWidget(self.addPagesLbl)
        
        #Choose book to update progress on
        self.combo = QComboBox(self) 
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
        ####################
        
        ###MenuBar#######
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
        
        newFile = QAction(QIcon('new_file.jpg'), '&New', self)
        newFile.setShortcut('Ctrl+N')
        newFile.setStatusTip ('Create a new bookshelf')
        newFile.triggered.connect(self.newShelf)
        
        self.statusBar()
        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newFile)
        fileMenu.addAction(openFile)
        fileMenu.addAction(saveFile)
        fileMenu.addAction(exitAct)
        ###########################
        
        #Show widgets
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
            with open(fname[0], mode='r', encoding="utf8") as csv_file:

                csv_reader = csv.DictReader(csv_file)
                line_count = 0
                for row in csv_reader:
                    if line_count == 0:
                        col_names = (f'Column names are {", ".join(row)}')
                        print (col_names)
                        line_count += 1
                    else:
            #print(f'\t{row["Book Id"]} works in the {row["Title"]} department, and was born in {row["Author"]}.')
                        line_count += 1
                        id_num = (f'{row["Book Id"]}')
                        title = f'{row["Title"]}'
                        author = f'{row["Author"]}'
                        pages = f'{row["Number of Pages"]}'
                        year = f'{row["Original Publication Year"]}'
                        book_dict = {"id_num" : id_num, "title" : title, "author" : author, "pages" : pages,
                         "year" : year}
                        self.bookShelf.append(book_dict)
                print(f'Processed {line_count} lines.')
                
    def onActivated(self, text):
    
        self.btn_progress.setText("Update the progress of: " + text)
        
    def addBooksFunc(self):
        '''Adds book to combo widget and changes label at the bottom to indicate added book'''
        '''Also adds these details to a data file'''
        title_new = self.addTitle.text()
        author_new = self.addAuthor.text()
        pages_new = self.addPages.text()
        if len(self.bookShelf) == 0:
            id_num = 1000000
        else:
            id_num = self.bookShelf[len(self.bookShelf)-1]["id"]+1 #Adds appropraite id to new book
            
            
        if title_new != "": ###Requires both Author and Book Title, if not, return message
            if author_new != "":
                self.added_book.setText("You have just added " + str(title_new) + " by " + 
                                        str(author_new) +
                                        " to your reading list")
                self.combo.addItem(str(title_new))
                newBookEntry = {"id": id_num, "title": title_new, "author": author_new, "pages": pages_new}
                self.bookShelf.append(newBookEntry)
            else:
                self.added_book.setText("Please add the author")
        else:
            self.added_book.setText("Please add a title")
        #print (self.bookShelf)
            
    def newShelf(self):
        self.bookShelf = []
        self.added_book.setText("Please add books to your new bookshelf.")
            
    def addProgress(self, index):
        '''Requests new page number in dialog, adds new page number with book id, 
        title and date to new dictionary entry. Prints the update to console and changes label'''
        text, ok = QInputDialog.getText(self, 'Input Dialog',  #Dialog title, Dialog message
            'Enter new page:') #Returns text and a boolean value (TRUE or FALSE)
        
        if ok:
            self.added_book.setText("You are now on page " + str(text) + " of " + 
                                    str(self.combo.itemText(index))) 
            #Sets text of QLabel
        
            datetime = QDateTime.currentDateTime()
            for i in range(len(self.bookShelf)):
                if "title" in self.bookShelf[i]:
                    id_bookUpdated = (self.bookShelf[i]["id"])
            added_update = {"date": datetime, "id": id_bookUpdated, "title": self.combo.itemText(index),
                            "progress": text}
            print (added_update)
            self.updates.append(added_update)
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ReadingApp()
    sys.exit(app.exec_())