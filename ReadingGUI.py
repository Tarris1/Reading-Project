# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 19:27:49 2018

@author: Sandsnes
"""

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

class ReadingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'You and your Reading'
        self.left = 300
        self.top = 500
        self.width = 1000
        self.height = 500
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        #self.createTable()
 
        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QVBoxLayout()
        #self.layout.addWidget(self.tableWidget) 
        self.setLayout(self.layout) 
 
        # Show widget
        self.show()
    
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ReadingApp()
    sys.exit(app.exec_())