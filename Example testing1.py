# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 18:10:10 2018

@author: Sandsnes
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QGridLayout, QLabel, QLineEdit
                             , QMessageBox, QPushButton, QTextEdit, QVBoxLayout
                             , QWidget, QTableView, QTableWidget,QTableWidgetItem, QApplication, QMainWindow)



class AddressBook(QWidget):
    def __init__(self, parent=None):
        super(AddressBook, self).__init__(parent)

        nameLabel = QLabel("Name of book:")
        self.nameLine = QLineEdit()
        #self.nameLine.setReadOnly(True) Cannot add text

        authorLabel = QLabel("Author Name:")
        self.authorText = QTextEdit()
        #self.authorText.setReadOnly(True) Cannot add text
        
        statLabel = QLabel("Reading Statistics")
        
        self.addButton = QPushButton("&Add")
        self.addButton.show()
        
        buttonLayout1 = QVBoxLayout()
        buttonLayout1.addWidget(self.addButton, Qt.AlignTop)
        
        table = QTableWidget(3, 3,self)  # create 3x3 table
        table.setHorizontalHeaderLabels(('Col 1', 'Col 2', 'Col 3'))
        table.setVerticalHeaderLabels(('Row 1', 'Row 2', 'Row 3'))
        

        mainLayout = QGridLayout()
        mainLayout.addWidget(nameLabel, 0, 0)
        mainLayout.addWidget(self.nameLine, 0, 1)
        mainLayout.addWidget(authorLabel, 1, 0) #Qt.AlignTop)
        mainLayout.addWidget(self.authorText, 1, 1)
        mainLayout.addWidget(statLabel,0,2)
        mainLayout.addLayout(buttonLayout1, 2, 1)
        
        
        

        self.setLayout(mainLayout)
        self.setWindowTitle("Adding a book")
        

if __name__ == '__main__':
    import sys

    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    addressBook = AddressBook()
    addressBook.show()

    sys.exit(app.exec_())
