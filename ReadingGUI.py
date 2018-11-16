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
                             qApp, QInputDialog, QFileDialog, QTextEdit, QComboBox, QShortcut,QGridLayout)
                             
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
        self.btn_add_books.setShortcut('Ctrl+E')
        self.btn_add_books.clicked.connect(self.addBooksFunc)
        
        self.changeShelfBtn = QPushButton('Change Shelf', self)
        
        self.add_booksLbl = QLabel("Add the details of the new book below:", self)
        self.added_book = QLabel('', self) #Label indicating added book 
        
        #Change Shelf
        self.changeShelfLbl = QLabel("Change shelf of book")
        self.changeShelfCombo = QComboBox(self)
        self.changeShelfTo = QComboBox(self)
        self.changeShelfTo.addItems(["to-read", "currently-reading", "read"])
        self.changeShelfBtn = QPushButton('Change Shelf', self)
        self.changeShelfBtn.clicked.connect(self.changeShelfFunc)
        
        changeShelfBox = QVBoxLayout()
        changeShelfBox.addWidget(self.changeShelfLbl)
        changeShelfBox.addWidget(self.changeShelfCombo)
        changeShelfBox.addWidget(self.changeShelfTo)
        changeShelfBox.addWidget(self.changeShelfBtn)
        
        
        TopHBox = QHBoxLayout()
        TopHBox.addWidget(self.add_booksLbl)
        
        
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
        
        self.bookStatus = QComboBox(self)
        self.bookStatus.addItems(["To-read", "Currently-Reading", "Read"])
        bookStatusBox = QHBoxLayout()
        
        addBookHBox = QHBoxLayout()
        addBookHBox.addWidget(self.btn_add_books)
        
        addedBookCommentBox = QHBoxLayout()
        addedBookCommentBox.addWidget(self.added_book)
        
        #Choose book to update progress on
        self.combo = QComboBox(self) 
        self.combo.activated[str].connect(self.onActivated) 
        
        
        ProgresshBox = QHBoxLayout()
        ProgresshBox.addWidget(self.combo)
        ProgresshBox.addWidget(self.btn_progress)
        #ProgresshBox.addLayout(changeShelfBox)
        
        
        addingNewBookVBox = QVBoxLayout() 
        addingNewBookVBox.addLayout(TopHBox)
        addingNewBookVBox.addLayout(titleHbox)
        addingNewBookVBox.addLayout(AuthorHbox)
        addingNewBookVBox.addLayout(PagesHbox)
        addingNewBookVBox.addLayout(bookStatusBox) #Combo box for shelf
        addingNewBookVBox.addLayout(addBookHBox)
        addingNewBookVBox.addWidget(self.added_book) 
        addingNewBookVBox.addStretch(1)
        addingNewBookVBox.addLayout(changeShelfBox)
        addingNewBookVBox.addStretch(1)
        addingNewBookVBox.addLayout(ProgresshBox)
        #addingNewBookVBox.setMargin(0)
        
               
        tab1 = QWidget(self) #First Tab
        self.setCentralWidget(tab1)
        tab1.setLayout(addingNewBookVBox)
        ####################
        
        ###MenuBar#######
        exitAct = QAction(QIcon('exit24.png'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q') #Short cut for exiting app
        exitAct.setStatusTip('Exit application') #When hovering over exit option, show message
        exitAct.triggered.connect(qApp.quit) #Adds the function to the menu option
        
        saveFile = QAction(QIcon('save.png'), '&Save', self)
        saveFile.setShortcut('Ctrl+S')
        saveFile.setStatusTip('Save your data')
        saveFile.triggered.connect(self.saveBookShelf)
        
        openFile = QAction(QIcon('open.png'), 'Import a bookshelf from Goodreads', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.openFileDialog)
        
        newFile = QAction(QIcon('new_file.jpg'), '&Create a new bookshelf', self)
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
            
    def openFileDialog(self): 
        '''Opens a Goodreads shelf, extracts book id, title, author, page number,
        publication year, ISBN, ISBN13'''
        fname = QFileDialog.getOpenFileName(self, 'Import a goodreads bookshelf', '/home')

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
                        ISBN = f'{row["ISBN"]}'
                        ISBN13 = f'{row["ISBN13"]}'
                        Bookshelves = f'{row["Bookshelves"]}'
                        self.changeShelfCombo.addItem(str(title))
                        if "currently-reading" in Bookshelves: 
                            #Adds only books on currently reading list to combo box
                            self.combo.addItem(str(title))
                        if self.combo.count()>0:
                            index = self.combo.count()+1
                        else:
                            index = line_count-1
                        book_dict = {"Book Id" : id_num, "Title" : title, "Author" : author, 
                                     "Number of Pages" : pages, "Bookshelves" : Bookshelves,
                         "Original Publication Year" : year, "ISBN": ISBN, "ISBN13": ISBN13, "id": index}
                        self.bookShelf.append(book_dict) #Adds to combo bar
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
            id_num = 1
        else:
            id_num = self.bookShelf[len(self.bookShelf)-1]["id"]+1 #Adds appropraite id to new book
            
            
        if title_new != "" and author_new != "" and self.bookStatus.currentText() != "": ###Requires both Author and Book Title, if not, return message
            #if author_new != "":
            self.added_book.setText("You have just added " + str(title_new) + " by " + 
                                        str(author_new) +
                                        " to your reading list")
            bookStatus = self.bookStatus.currentText()
            if "currently-reading" in bookStatus.lower(): 
                #Only books currently to read is added to combo widget
                self.combo.addItem(str(title_new))
            
            newBookEntry = {"id": id_num, "Title": title_new, "Author": author_new, 
                                "Number of Pages": pages_new, "Bookshelves": bookStatus}
            self.bookShelf.append(newBookEntry)
            self.changeShelfCombo.addItem(str(title_new))
        elif title_new == "" and author_new != "":
            self.added_book.setText("Please add the author")
        elif title_new != "" and author_new == "":
            self.added_book.setText("Please add a title")
        
            
    def newShelf(self):
        '''Clears the bookshelf list, tells the user that shelf is cleared if a bookshelf existed before,
        else tells the user that a bookshelf, clears combo box'''
        self.bookShelf = []
        if len(self.combo.currentText()) >0:
            self.added_book.setText("Your shelf is now cleared. Please add books")
        else:
            self.added_book.setText("A bookshelf has been created. Please add books to your new bookshelf.")
        self.combo.clear()
        
            
    def addProgress(self, index):
        '''Requests new page number in dialog, adds new page number with book id, 
        title and date to new dictionary entry. Prints the update to console and changes label'''
        bookToUpdate = str(self.combo.currentText())
        InputText = ""
        datetime = QDateTime.currentDateTime()
        #datetime = datetime.toString()
        
        if len(bookToUpdate)==0:
            InputText = "You have no book to update"
        else:
            InputText = 'What page of ' + bookToUpdate + ' are you on?'
        
        text, ok = QInputDialog.getText(self, 'Input Dialog',  #Dialog title, Dialog message
            InputText) #Returns text and a boolean value (TRUE or FALSE)
        
        if ok and len(self.combo.currentText())>0 and len(text)>0:
            #bookToUpdate = str(self.combo.currentText())
            self.added_book.setText("You are now on page " + str(text) + " of " + 
                                    bookToUpdate) 
            #Sets text of QLabel
        
            #datetime = QDateTime.currentDateTime()
            for i in range(len(self.bookShelf)):
                if self.bookShelf[i]["Title"] == bookToUpdate:
                    id_bookUpdated = (self.bookShelf[i]["id"])
                    if int(text) >= int(self.bookShelf[i]["Number of Pages"]): 
                        '''if new page number exceeds pages in the book, 
                        change shelf to "Read" and remove finished book from combo box '''
                        self.combo.removeItem(self.combo.currentIndex())
                        self.added_book.setText("Congratulations! You have now finished "+ 
                                                bookToUpdate + "!")
                        self.bookShelf[i].update({"Bookshelves": "Read" })
                        print(self.bookShelf[i])
                        text = int(self.bookShelf[i]["Number of Pages"])
                        
                    added_update = {"date": datetime, "id": id_bookUpdated, "Title": bookToUpdate,
                            "progress": text}
                    self.updates.append(added_update)
            print (self.updates)
        elif ok and len(text)==0:
            self.added_book.setText("Please enter a page number")
        else:
            self.added_book.setText("Error: There are no books to update")
        
    def saveBookShelf(self):
        '''Saves bookshelf to selected folder as a CSV file'''
        save = QFileDialog.getSaveFileName(self, 'Save file', '/home')
        
        if save[0]:
            with open(save[0]+'.csv', mode='w', encoding = "utf8", newline='') as csv_file:
                fieldnames = ['id', 'Book Id', 'Title', 'Author', 'Number of Pages', 
                              'Original Publication Year', 'ISBN', 'ISBN13']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                for i in range(len(self.bookShelf)):
                    writer.writerow(self.bookShelf[i])
    def changeShelfFunc(self):
        '''Changes shelf of book selected and adds book to progress combo box if currently-reading is selelected'''
        print (self.changeShelfTo.currentText())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ReadingApp()
    sys.exit(app.exec_())