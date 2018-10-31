# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 19:27:49 2018

@author: Sandsnes
"""

import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget,
                             QAction, QTableWidget,QTableWidgetItem,QVBoxLayout, QLabel, QLineEdit, QPushButton)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

class ReadingApp(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("My Reading App")
        self.left = 50
        self.top = 100
        self.width = 1000
        self.height = self.width
        self.setGeometry(self.left, self.top, self.width, self.height)
        btn = QPushButton('Update Progress', self)
        btn.setToolTip('Update your reading progress')
        btn.resize(btn.sizeHint())
        btn.move(50,self.height-250)
        btn_add_books = QPushButton('Add a New Book', self)
        btn_add_books.setToolTip ('Add a new book to your shelf')
        btn_add_books.resize(btn.sizeHint())
        btn_add_books.move(50, self.height-100) #Add the bottom of the app
        
        
 
        # Show widget
        self.show()
    
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ReadingApp()
    sys.exit(app.exec_())