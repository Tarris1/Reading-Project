# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 18:16:19 2018

@author: Sandsnes
"""
def enter_book():
#Queries for details of book
    Title_new_book = input ("Add a new book title:")
    Author_new_book = input("Who wrote the book?")
    Pages_new_book = input("How many pages does the book contain?")
    print ("The book you entered is called \"%s\" by %s and contains %s pages" % \
               (Title_new_book,Author_new_book,Pages_new_book))

    New_number = Number_index.append(len(Number_index)+1)
    New_title = Titles_index.append(Title_new_book)
    New_author = Author_index.append(Author_new_book)
    New_pages = Pages_index.append(int(Pages_new_book))
    Books_index = [Number_index,Titles_index,Author_index,Pages_index]
