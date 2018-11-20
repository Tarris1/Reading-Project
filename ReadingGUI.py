# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 19:27:49 2018

@author: Sandsnes
"""

import sys
import csv
import operator
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget,
                             QAction,QVBoxLayout, QHBoxLayout, QTextEdit,
                             QLabel, QLineEdit, QPushButton, QTabWidget,
                             qApp, QInputDialog, QFileDialog, QComboBox, QTableView, QTableWidget, QTableWidgetItem)
                             
from PyQt5.QtGui import QIcon, QStandardItemModel
from PyQt5.QtCore import QDateTime, QAbstractTableModel



class ReadingApp(QMainWindow):
    def __init__(self):
        
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        
        self.bookShelf = [] #Initiate bookshelf list
        self.updates = [] #Initiate update list
        self.currentlyReadingShelf = [] #Initiate currently reading shelf
        self.booksReadShelf = [] #Initiate read books shelf
        self.tabledata = [] #Initiate table data list
        
        ##################Widgets##################
        self.btn_progress = QPushButton('Update Progress', self) #Add Progress button
        self.btn_progress.setToolTip('Update your reading progress')
        self.btn_progress.clicked.connect(self.addProgress)
        
        self.btn_add_books = QPushButton('Add a New Book', self) ###Add a new Book button
        self.btn_add_books.setToolTip ('Add a new book to your shelf')
        #self.btn_add_books.clicked.connect (self.showDialog) #Opens up a dialog where you can "add" books
        self.btn_add_books.setShortcut('Ctrl+E')
        self.btn_add_books.clicked.connect(self.addBooksFunc)
        
        self.btnFinishedBook = QPushButton("Finished the book? Click here.", self)
        self.btnFinishedBook.clicked.connect(self.finishedBook)
        self.updatedBookLbl = QLabel("", self)
        
        self.statisticsButton = QPushButton('Click here for Statistics', self)
        self.statisticsButton.clicked.connect(self.bookStatistics)
        self.statisticsLbl = QLabel("", self)
        
        self.changeShelfBtn = QPushButton('Change Shelf', self)
        
        self.add_booksLbl = QLabel("Add the details of the new book below:", self)
        self.added_book = QLabel('', self) #Label indicating added book 
        
        #Change Shelf widgets
        self.changeShelfLbl = QLabel("Change shelf of book")
        self.changeShelfCombo = QComboBox(self)
        self.changeShelfTo = QComboBox(self)
        self.changeShelfTo.addItems(["to-read", "currently-reading", "read"])
        self.changeShelfBtn = QPushButton('Change Shelf', self)
        self.changeShelfBtn.clicked.connect(self.changeShelfFunc)
        
        #Filter functionality
        self.filterOptions = [">=", "=", ">", "<", "<=", ""]
        self.filterBox = QHBoxLayout()
        
        self.filterEditBoxOne = QVBoxLayout()
        self.filterEditBoxComboOne = QVBoxLayout()
        
        self.filterEditBoxTwo = QVBoxLayout()
        self.filterEditBoxComboTwo = QVBoxLayout()
        
        self.filterEditPagesOne = QLineEdit(self)
        self.filterEditPagesTwo = QLineEdit(self)
        self.filterEditPagesOneCombo = QComboBox(self)
        self.filterEditPagesOneCombo.addItems(self.filterOptions)
        self.filterEditPagesTwoCombo = QComboBox(self)
        self.filterEditPagesTwoCombo.addItems(self.filterOptions)
        self.filterEditPagesLbl = QLabel("Select range of pages")
        self.filterEditYearOne = QLineEdit(self)
        self.filterEditYearTwo = QLineEdit(self)
        self.filterEditYearOneCombo = QComboBox(self)
        self.filterEditYearOneCombo.addItems(self.filterOptions)
        self.filterEditYearTwoCombo = QComboBox(self)
        self.filterEditYearTwoCombo.addItems(self.filterOptions)
        self.filterEditYearLbl = QLabel("Select range of publication years")
        
        self.filterEditBoxOne.addWidget(self.filterEditPagesOne)
        self.filterEditBoxOne.addWidget(self.filterEditYearOne)
        self.filterEditBoxComboOne.addWidget(self.filterEditPagesOneCombo)
        self.filterEditBoxComboOne.addWidget(self.filterEditYearOneCombo)
        
        self.filterEditBoxTwo.addWidget(self.filterEditPagesTwo)
        self.filterEditBoxTwo.addWidget(self.filterEditYearTwo)
        self.filterEditBoxComboTwo.addWidget(self.filterEditPagesTwoCombo)
        self.filterEditBoxComboTwo.addWidget(self.filterEditYearTwoCombo)
        
        self.filterBtn = QPushButton("Click here to filter")
        self.filterBtn.clicked.connect(self.filterTableFunc)
        ###################################
        
        self.filterLabelBox = QVBoxLayout()
        self.filterLabelBox.addWidget(self.filterEditPagesLbl)
        self.filterLabelBox.addWidget(self.filterEditYearLbl)
        
        self.filterBox.addLayout(self.filterLabelBox)
        self.filterBox.addLayout(self.filterEditBoxOne)
        self.filterBox.addLayout(self.filterEditBoxComboOne)
        
        self.filterBox.addLayout(self.filterEditBoxTwo)
        self.filterBox.addLayout(self.filterEditBoxComboTwo)
        #self.filterBox.addWidget(self.filterBtn)
        
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
        self.bookStatus.addItems(["to-read", "currently-reading", "read"])
        
        #Choose book to update progress on
        self.combo = QComboBox(self) 
        self.combo.activated[str].connect(self.onActivated) 
        
        addBookHBox = QHBoxLayout()
        addBookHBox.addWidget(self.btn_add_books)
        
        addedBookCommentBox = QHBoxLayout()
        addedBookCommentBox.addWidget(self.added_book)
        
        addNewBookBox = QVBoxLayout()
        addNewBookBox.addWidget(self.add_booksLbl)
        addNewBookBox.addLayout(titleHbox)
        addNewBookBox.addLayout(AuthorHbox)
        addNewBookBox.addLayout(PagesHbox)
        addNewBookBox.addWidget(self.bookStatus)
        addNewBookBox.addLayout(addBookHBox)
        addNewBookBox.addWidget(self.added_book)
        
        self.changeShelfBox = QVBoxLayout()
        self.changeShelfBox.addWidget(self.changeShelfLbl)
        self.changeShelfBox.addWidget(self.changeShelfCombo)
        self.changeShelfBox.addWidget(self.changeShelfTo)
        self.changeShelfBox.addWidget(self.changeShelfBtn)
        
        ProgresshBox = QHBoxLayout()
        #ProgresshBox.addWidget(self.combo)
        ProgresshBox.addWidget(self.btn_progress)
        ProgresshBox.addWidget(self.btnFinishedBook)
        
        
        mainColumn = QVBoxLayout() 
        mainColumn.addLayout(addNewBookBox)
        mainColumn.addStretch(1)
        mainColumn.addWidget(self.combo)
        mainColumn.addLayout(ProgresshBox)
        mainColumn.addWidget(self.updatedBookLbl)
        #mainColumn.addStretch(1)
    
        statisticsBox = QVBoxLayout()
        statisticsBox.addWidget(self.statisticsButton)
        statisticsBox.addWidget(self.statisticsLbl)
        statisticsBox.addStretch(1)
        
        ##2nd Tab
        self.shelfBox = QVBoxLayout()
        self.shelfBox.addLayout(self.changeShelfBox)
        self.shelfBox.addStretch(1)
        self.shelfBox.addLayout(self.filterBox)
        self.shelfBox.addWidget(self.filterBtn)
        #self.shelfBox.addStretch(1)
        
        
        
        self.layout = QVBoxLayout(self)
        
        #Create tabs and QTabWidget
        self.addBookTab = QWidget()
        self.yourBookShelf = QWidget()
        self.statisticsTab = QWidget()
        self.tabs = QTabWidget()
        self.tabs.setMovable(True)
        
        #set layout of tab 1
        self.addBookTab.layout = QVBoxLayout()
        self.addBookTab.layout.addLayout(mainColumn)      
        self.addBookTab.setLayout(self.addBookTab.layout)
        
        #set layout of tab 2
        self.yourBookShelf.layout = QVBoxLayout()
        self.yourBookShelf.layout.addLayout(self.shelfBox)
        self.yourBookShelf.setLayout(self.yourBookShelf.layout)
        
        #set layout of tab 3
        self.statisticsTab.layout = QVBoxLayout()
        self.statisticsTab.layout.addLayout(statisticsBox)
        self.statisticsTab.setLayout(self.statisticsTab.layout)
        
        #Add tabs to window
        self.tabs.addTab(self.addBookTab, "Add Books")
        self.tabs.addTab(self.yourBookShelf, "Your bookshelf")
        self.tabs.addTab(self.statisticsTab, "Reading Statistics")
        

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        self.setCentralWidget(self.tabs)
        
        #tab1 = QWidget(self) #First Tab
        #self.setCentralWidget(tab1)
        #tab1.setLayout(mainColumn)
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
        createTable = True
        
        if self.combo.count()>0:
            index = self.combo.count()
        else:
            index = 0
        fname = QFileDialog.getOpenFileName(self, 'Import a goodreads bookshelf', '/home')

        if len(self.tabledata)>0:
            createTable = False


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
                        if pages != "":
                            pages = int(pages)
                        elif pages == "":
                            pages = 1
                        
                        year = f'{row["Original Publication Year"]}'
                        if year != "":
                            year = int(year)
                        elif year == "":
                            year = 1
                        ISBN = f'{row["ISBN"]}'
                        ISBN13 = f'{row["ISBN13"]}'
                        Bookshelves = f'{row["Bookshelves"]}'
                        if "to-read" in Bookshelves: ###Remove all random bookshelves in goodreads
                            Bookshelves = "to-read"
                        elif "currently-reading" in Bookshelves:
                            Bookshelves = "currently-reading"
                        else:
                            Bookshelves = "read"
                            
                        dateRead = f'{row["Date Read"]}'
                        myReview = f'{row["My Review"]}'
                        self.changeShelfCombo.addItem(str(title))
                        index = index + 1

                        book_dict = {"Book Id" : id_num, "Title" : title, "Author" : author, 
                                     "Number of Pages" : pages, "Bookshelves" : Bookshelves,
                         "Original Publication Year" : year, "ISBN": ISBN, "ISBN13": ISBN13, "id": index,
                         "Date Read": dateRead, "My Review": myReview}
                        row_data = [index, title, author, pages, Bookshelves, year] #Also makes a list of lists version
                        self.tabledata.append(row_data) #appends to tabledata
                        if "currently-reading" in Bookshelves: 
                            #Adds only books on currently reading list to combo box
                            self.combo.addItem(str(title))
                            self.currentlyReadingShelf.append(book_dict)
                        self.bookShelf.append(book_dict) #Adds to combo bar
                        if dateRead != "":
                            self.booksReadShelf.append(book_dict)
                print(f'Processed {line_count} lines.')
                print (len(self.booksReadShelf))
        
        '''create & add table of the bookshelf if it does not exist already, 
        else update existing table'''
        if createTable != False:
            self.table = self.createTable(self.tabledata) #Creates the table
            self.shelfBox.addWidget(self.table) #Adds table to second tab
        else:
            self.table.model().layoutChanged.emit()
        

                
    def createTable(self, data):
        # create the view
        tv = QTableView()
        colWidth = 8
        # set the table model
        self.header = ['id', 'Title', 'Author', 'Number of Pages', 'Bookshelves', 'Original Publication Year']
        self.tableModel = MyTableModel(data, self.header, self)
        tv.setModel(self.tableModel)

        # set the minimum size
        tv.setMinimumSize(400, 300)

        # hide grid
        tv.setShowGrid(True)

        # hide vertical header
        vh = tv.verticalHeader()
        vh.setVisible(False)

        # set horizontal header properties
        hh = tv.horizontalHeader()
        hh.setStretchLastSection(True)

        # set column width to fit contents
        tv.resizeColumnsToContents()
        tv.setColumnWidth(1, colWidth)

        # set row height
        tv.resizeRowsToContents()

        # enable sorting
        tv.setSortingEnabled(True)

        return tv   
                
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
            newBookEntry = {"id": id_num, "Title": title_new, "Author": author_new, 
                                "Number of Pages": pages_new, "Bookshelves": bookStatus}
            self.bookShelf.append(newBookEntry)
            self.changeShelfCombo.addItem(str(title_new))
            if pages_new != "":
                pages_new = int(pages_new)
            elif pages_new == "":
                pages_new = 1
            row_data = [id_num, title_new, author_new, int(pages_new), bookStatus, ""] #Also makes a list of lists version
            data.append(row_data) #appends to tabledata
            
            if "currently-reading" in bookStatus.lower(): 
                #Only books currently to read is added to combo widget
                self.combo.addItem(str(title_new))
                self.currentlyReadingShelf.append(newBookEntry)
                print (self.currentlyReadingShelf)
            if len(self.tabledata)>1:
                self.table.model().layoutChanged.emit()
            elif len(self.tabledata)==1:
                self.table = self.createTable(self.tabledata) #Creates the table
                self.shelfBox.addWidget(self.table) #Adds table to second tab
                
                
        elif title_new == "" and author_new != "":
            self.added_book.setText("Please add the author")
        elif title_new != "" and author_new == "":
            self.added_book.setText("Please add a title")
        
            
    def newShelf(self):
        '''Clears the bookshelf list, tells the user that shelf is cleared if a bookshelf existed before,
        else tells the user that a bookshelf, clears combo box'''
        self.bookShelf = []
        self.tabledata = []
        if len(self.combo.currentText()) >0:
            self.added_book.setText("Your shelf is now cleared. Please add books")
        else:
            self.added_book.setText("A bookshelf has been created. Please add books to your new bookshelf.")
        self.combo.clear()
        
        #self.table.model().layoutChanged.emit()
        
            
    def addProgress(self, index):
        '''Requests new page number in dialog, adds new page number with book id, 
        title and date to new dictionary entry. Prints the update to console and changes label'''
        bookToUpdate = str(self.combo.currentText())
        InputText = ""
        datetime = QDateTime.currentDateTime()
        updateOrNot = False
        #datetime = datetime.toString()
        
        if len(bookToUpdate)==0:
            InputText = "You have no book to update"
        else:
            InputText = 'What page of ' + bookToUpdate + ' are you on?'
        
        text, ok = QInputDialog.getText(self, 'Input Dialog',  #Dialog title, Dialog message
            InputText) #Returns text and a boolean value (TRUE or FALSE)
        
        if ok and len(self.combo.currentText())>0 and len(text)>0:
            #bookToUpdate = str(self.combo.currentText())
            self.updatedBookLbl.setText("You are now on page " + str(text) + " of " + 
                                    bookToUpdate) 
            #Sets text of QLabel
            for i in range(len(self.currentlyReadingShelf)):
                print(i)
                if self.currentlyReadingShelf[i]["Title"] == bookToUpdate:
                    id_bookUpdated = self.currentlyReadingShelf[i]["id"]
                    if int(text) >= int(self.currentlyReadingShelf[i]["Number of Pages"]):
                        self.combo.removeItem(self.combo.currentIndex())
                        self.updatedBookLbl.setText("Congratulations! You have now finished "+ 
                                                bookToUpdate + "!")
                        self.bookShelf[id_bookUpdated-1].update({"Bookshelves": "Read"})
                        self.bookShelf[id_bookUpdated-1].update({"Date Read": datetime})
                        #del self.currentlyReadingShelf[i]
                        print (self.bookShelf[id_bookUpdated-1])
                        bookToRemove = i
                        updateOrNot = True
                        text = int(self.currentlyReadingShelf[i]["Number of Pages"])
                        
                    added_update = {"date": datetime, "id": id_bookUpdated, "Title": bookToUpdate,
                            "progress": text}
                    self.updates.append(added_update)
            if updateOrNot == True:
                del self.currentlyReadingShelf[bookToRemove]                      
            self.btn_progress.setText("Update the progress of: " + self.combo.currentText())
        elif ok and len(text)==0:
            self.updatedBookLbl.setText("Please enter a page number")
        else:
            self.updatedBookLbl.setText("Error: There are no books to update")
            
        
    def saveBookShelf(self):
        '''Saves bookshelf to selected folder as a CSV file'''
        save = QFileDialog.getSaveFileName(self, 'Save file', '/home')
        
        if save[0]:
            with open(save[0]+'.csv', mode='w', encoding = "utf8", newline='') as csv_file:
                fieldnames = ['id', 'Book Id', 'Title', 'Author', 'Number of Pages', 
                              'Original Publication Year', 'ISBN', 'ISBN13',
                              "Bookshelves", "Date Read", "My Review"]
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                for i in range(len(self.bookShelf)):
                    writer.writerow(self.bookShelf[i])
    def changeShelfFunc(self):
        '''Changes shelf of book selected and adds book to progress combo box 
        if currently-reading is selelected'''
        print (self.changeShelfTo.currentText())
    
    
      
    def finishedBook(self):
        '''Opens a review dialog, removes finished book from combo widget, 
        changes bookshelf to "read" and adds progress to progress list'''
        bookToUpdate = str(self.combo.currentText())
        datetime = QDateTime.currentDateTime()
        updateOrNot = False
        
        inputText = ("Did you finish " + bookToUpdate + "? If so, feel free to add a review below")
        
        text, ok = QInputDialog.getMultiLineText(self, 'input Dialog', inputText)
        if ok and len(self.combo.currentText())>0 and len(text)>=0:
            self.updatedBookLbl.setText("You are now on page " + str(text) + " of " + 
                                    bookToUpdate) 
            #Sets text of QLabel
            for i in range(len(self.currentlyReadingShelf)):
                print(i)
                if self.currentlyReadingShelf[i]["Title"] == bookToUpdate:
                    id_bookUpdated = self.currentlyReadingShelf[i]["id"]
                    self.combo.removeItem(self.combo.currentIndex())
                    self.updatedBookLbl.setText("Congratulations! You have now finished "+ 
                                                bookToUpdate + "!")
                    self.bookShelf[id_bookUpdated-1].update({"Bookshelves": "Read"})
                    self.bookShelf[id_bookUpdated-1].update({"Date Read": datetime})
                    self.bookShelf[id_bookUpdated-1].update({"My Review": text})
                        #del self.currentlyReadingShelf[i]
                    print (self.bookShelf[id_bookUpdated-1])
                    bookToRemove = i
                    updateOrNot = True
                    pages_read = int(self.currentlyReadingShelf[i]["Number of Pages"])
                    
                        
                    added_update = {"date": datetime, "id": id_bookUpdated, "Title": bookToUpdate,
                            "progress": pages_read, "review": text}
                    self.updates.append(added_update)
                    print (self.updates)
                    print
            if updateOrNot == True:
                del self.currentlyReadingShelf[bookToRemove]                      
            self.btn_progress.setText("Update the progress of: " + self.combo.currentText())
        else:
            self.updatedBookLbl.setText("")    
        
    def bookStatistics(self):
        '''Prints out statistics'''
        booksToAnalyze = self.bookShelf
        page_read = 0
        ###Extract books read:
        for i in range(len(booksToAnalyze)):
            bookShelves = booksToAnalyze[i]["Bookshelves"]
            if not ("currently-reading") in bookShelves and not ("to-read") in bookShelves or "Read" in bookShelves:
                pageOfBookI = booksToAnalyze[i]["Number of Pages"]
                if len(pageOfBookI)>0:
                    page_read = page_read+int(booksToAnalyze[i]["Number of Pages"])
        self.statisticsLbl.setText("You have a read a total of " + str(page_read) + 
                                   " pages since you started reading.")
        
    def filterTableFunc(self):
        '''filters the data table and updates table'''
        self.filteredData = []
        self.originalModel = self.tabledata
        filtPagesOne = self.filterEditPagesOneCombo.currentText()
        filtPagesTwo = self.filterEditPagesTwoCombo.currentText()
        filtYearOne = self.filterEditYearOneCombo.currentText()
        filtYearTwo = self.filterEditYearTwoCombo.currentText()
        if self.filterEditPagesOne.displayText() != "":
            pagesOne = int(self.filterEditPagesOne.displayText())
        else:
            pagesOne = ""
        if self.filterEditPagesTwo.displayText() != "":
            pagesTwo = int(self.filterEditPagesTwo.displayText())
        else: 
            pagesTwo = ""
        yearOne = self.filterEditYearOne.displayText()
        yearTwo = self.filterEditYearTwo.displayText()
        filters = [filtPagesOne, filtPagesTwo, filtYearOne, filtYearTwo]
        ranges = [pagesOne, pagesTwo, yearOne, yearTwo]
        print (ranges)
            
        #3rd position is pages, 5th position is publication year
        #Filter works fine, but table doesnt update - probably data is unchanged
        #self.table.model().layoutAboutToBeChanged.emit()
        
        '''Massive filter'''
        if pagesOne != "" or pagesTwo != "":
            for i in range(len(self.tabledata)):
                if filtPagesOne == ">=":
                    if int(self.tabledata[i][3]) >= pagesOne:
                        if filtPagesTwo == ">=":
                            if int(self.tabledata[i][3]) >= pagesTwo:
                                self.filteredData.append(self.tabledata[i])
                        if filtPagesTwo == "=":
                            if int(self.tabledata[i][3]) == pagesTwo:
                                self.filteredData.append(self.tabledata[i])
                        if filtPagesTwo == ">":
                            if int(self.tabledata[i][3]) > pagesTwo:
                                self.filteredData.append(self.tabledata[i])
                        if filtPagesTwo == "<=":
                            if int(self.tabledata[i][3]) <= pagesTwo:
                                self.filteredData.append(self.tabledata[i])
                        if filtPagesTwo == "<":
                            if int(self.tabledata[i][3]) < pagesTwo:
                                self.filteredData.append(self.tabledata[i])
                    
                if filtPagesOne == "=" or filtPagesTwo == "=":
                    if self.tabledata[i][3] == pagesOne or self.tabledata[i][3] == pagesTwo:
                        self.filteredData.append(self.tabledata[i])
            
                if filtPagesOne == ">":
                    if self.tabledata[i][3] > pagesOne:
                        if filtPagesTwo == ">=":
                            if int(self.tabledata[i][3]) >= pagesTwo:
                                self.filteredData.append(self.tabledata[i])
                        if filtPagesTwo == "=":
                            if int(self.tabledata[i][3]) == pagesTwo:
                                self.filteredData.append(self.tabledata[i])
                        if filtPagesTwo == ">":
                            if int(self.tabledata[i][3]) > pagesTwo:
                                self.filteredData.append(self.tabledata[i])
                        if filtPagesTwo == "<=":
                            if int(self.tabledata[i][3]) <= pagesTwo:
                                self.filteredData.append(self.tabledata[i])
                        if filtPagesTwo == "<":
                            if int(self.tabledata[i][3]) < pagesTwo:
                                self.filteredData.append(self.tabledata[i])
                    
                if filtPagesOne == "<=":
                    if self.tabledata[i][3] <= pagesOne:
                        if filtPagesTwo == ">=":
                            if int(self.tabledata[i][3]) >= pagesTwo:
                                self.filteredData.append(self.tabledata[i])
                        if filtPagesTwo == "=":
                            if int(self.tabledata[i][3]) == pagesTwo:
                                self.filteredData.append(self.tabledata[i])
                        if filtPagesTwo == ">":
                            if int(self.tabledata[i][3]) > pagesTwo:
                                self.filteredData.append(self.tabledata[i])
                        if filtPagesTwo == "<=":
                            if int(self.tabledata[i][3]) <= pagesTwo:
                                self.filteredData.append(self.tabledata[i])
                        if filtPagesTwo == "<":
                            if int(self.tabledata[i][3]) < pagesTwo:
                                self.filteredData.append(self.tabledata[i])
            
                if filtPagesOne == "<":
                    if self.tabledata[i][3] < pagesOne:
                        if filtPagesTwo == ">=":
                            if int(self.tabledata[i][3]) >= pagesTwo:
                                self.filteredData.append(self.tabledata[i])
                        if filtPagesTwo == "=":
                            if int(self.tabledata[i][3]) == pagesTwo:
                                self.filteredData.append(self.tabledata[i])
                        if filtPagesTwo == ">":
                            if int(self.tabledata[i][3]) > pagesTwo:
                                self.filteredData.append(self.tabledata[i])
                        if filtPagesTwo == "<=":
                            if int(self.tabledata[i][3]) <= pagesTwo:
                                self.filteredData.append(self.tabledata[i])
                        if filtPagesTwo == "<":
                            if int(self.tabledata[i][3]) < pagesTwo:
                                self.filteredData.append(self.tabledata[i])
                                
        #newModel = 
        if len(self.filteredData)>0:
            self.createTable(self.filteredData)
        #newModel = MyTableModel(self.filteredData, self.header, self)
            self.table.setModel(self.tableModel)
            self.table.model().layoutChanged.emit()
        

from PyQt5.QtCore import *
  
class MyTableModel(QAbstractTableModel):
    def __init__(self, datain, headerdata, parent=None):
        """
        Args:
            datain: a list of lists\n
            headerdata: a list of strings
        """
        QAbstractTableModel.__init__(self, parent)
        self.arraydata = datain
        self.headerdata = headerdata

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        if len(self.arraydata) > 0: 
            return len(self.arraydata[0]) 
        return 0

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
        return QVariant(self.arraydata[index.row()][index.column()])

    def setData(self, index, value, role):
        pass         # not sure what to put here
        
    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headerdata[col])
        return QVariant()  
    def sort(self, Ncol, order):
        """Sort table by given column number.
        """
        self.layoutAboutToBeChanged.emit()
        self.arraydata = sorted(self.arraydata, key=operator.itemgetter(Ncol))        
        if order == Qt.DescendingOrder:
            self.arraydata.reverse()
        self.layoutChanged.emit()

    



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ReadingApp()
    sys.exit(app.exec_())