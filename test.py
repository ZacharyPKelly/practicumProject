#IMPORTS
from ast import main
from asyncio import subprocess
from configparser import ConfigParser
from genericpath import isfile
import json
import os
from tkinter.messagebox import NO
import pkg_resources
import shutil
from shutil import make_archive
import sys
import subprocess
import platform

# print()
# print('-------------------------------------------------------------\n')
# print(os.name)
# print(platform.release())
# print()
# print('-------------------------------------------------------------')

###############################################################################################################################################################

# existingBooks = ['a', 'b', 'c', 'd', 'e', 'f', 'g']

# whichBookAnswer = True #True for staying in the loop, False for exiting the loop

# while whichBookAnswer == True: 

#     for i in range(len(existingBooks)):

#         print(i+1, ')', existingBooks[i])
                
#     print()

#     try:
#         whichBookOption = int(input('Enter your choice: '))
#     except:
#         print('Wrong input. Please enter a number between 1 and ', len(existingBooks), '.', sep=None)
                
#     if whichBookOption > 0 and whichBookOption <= len(existingBooks):

#         whichBookAnswer = False
#         bookToBeUploaded = existingBooks[whichBookOption-1]
                
#     else:

#         print("Invalid choice. Please enter a number between 1 and ", len(existingBooks), sep=None)
#         print()
#         print('Which Jupyter Book would you like to upload?\n')        

###############################################################################################################################################################

parent_dir = ""

owd = os.getcwd() #original working directory
#Local Repository Paths
jupyterDirectory = ""
jupyter = ""
jupyterBooks = ""
jupyterNotebooks = ""
notebookHTMLS = ""
zippedJupyterBooks = ""
jupyterImages = ""

#Eswatini Repository Paths
eswatiniRepository = ""
eswatiniRepositoryNotebooks = ""
eswatiniRepositoryHTML = ""
eswatiniRepositoryBooks = ""
eswatiniRepositoryZippedBooks = ""
eswatiniRepositoryImages = ""

try:
    parent_dir = os.path.expanduser('~')
    parent_dir = parent_dir + "\Documents"

    owd = os.getcwd() #original working directory
    #Local Repository Paths
    jupyterDirectory = os.path.join(parent_dir, "JupyterDirectory")
    jupyter = os.path.join(jupyterDirectory, "Jupyter")
    jupyterBooks = os.path.join(jupyter, "Books")
    jupyterNotebooks = os.path.join(jupyter, "Notebooks")
    notebookHTMLS = os.path.join(jupyterNotebooks, "NotebookHTMLs")
    zippedJupyterBooks = os.path.join(jupyterBooks, "ZippedBooks")
    jupyterImages = os.path.join(jupyter, "Images")

    #Eswatini Repository Paths
    eswatiniRepository = os.path.join(jupyterDirectory, "EswatiniRepository")
    eswatiniRepositoryNotebooks = os.path.join(eswatiniRepository, "static", "books", "juypterNotebooks")
    eswatiniRepositoryHTML = os.path.join(eswatiniRepository, "static", "books", "jupyterNotebookHTML")
    eswatiniRepositoryBooks = os.path.join(eswatiniRepository, "static", "books", "juypterBooks")
    eswatiniRepositoryZippedBooks = os.path.join(eswatiniRepository, "static", "books", "zippedJuypterBooks")
    eswatiniRepositoryImages = os.path.join(eswatiniRepository, "static", "Img")

    #creating Jupyter Directory
    os.mkdir(jupyterDirectory)

    #Creating folder to hold Jupyter Books and Jupyter Notebooks folders
    os.mkdir(jupyter)

    #Creating folder to hold Jupyter Books 
    os.mkdir(jupyterBooks)

    #Creating folder to hold Jupyter Notebooks
    os.mkdir(jupyterNotebooks)

    #Creating folder to hold zipped Jupyter Books
    os.mkdir(zippedJupyterBooks)

    #Creating folder to hold Jupyter Notebook HTML files
    os.mkdir(notebookHTMLS)

    #Creating folder to hold images for Notebook/Book Covers
    os.mkdir(jupyterImages)

    #Creating folder to hold Eswatini Repository
    os.mkdir(eswatiniRepository)

except:

    parent_dir = os.path.expanduser('~')
    parent_dir = parent_dir + "\Documents"

    owd = os.getcwd() #original working directory
    #Local Repository Paths
    jupyterDirectory = os.path.join(parent_dir, "JupyterDirectory")
    jupyter = os.path.join(jupyterDirectory, "Jupyter")
    jupyterBooks = os.path.join(jupyter, "Books")
    jupyterNotebooks = os.path.join(jupyter, "Notebooks")
    notebookHTMLS = os.path.join(jupyterNotebooks, "NotebookHTMLs")
    zippedJupyterBooks = os.path.join(jupyterBooks, "ZippedBooks")
    jupyterImages = os.path.join(jupyter, "Images")

    #Eswatini Repository Paths
    eswatiniRepository = os.path.join(jupyterDirectory, "EswatiniRepository")
    eswatiniRepositoryNotebooks = os.path.join(eswatiniRepository, "static", "books", "juypterNotebooks")
    eswatiniRepositoryHTML = os.path.join(eswatiniRepository, "static", "books", "jupyterNotebookHTML")
    eswatiniRepositoryBooks = os.path.join(eswatiniRepository, "static", "books", "juypterBooks")
    eswatiniRepositoryZippedBooks = os.path.join(eswatiniRepository, "static", "books", "zippedJuypterBooks")
    eswatiniRepositoryImages = os.path.join(eswatiniRepository, "static", "Img")

    #creating Jupyter Directory
    os.mkdir(jupyterDirectory)

    #Creating folder to hold Jupyter Books and Jupyter Notebooks folders
    os.mkdir(jupyter)

    #Creating folder to hold Jupyter Books 
    os.mkdir(jupyterBooks)

    #Creating folder to hold Jupyter Notebooks
    os.mkdir(jupyterNotebooks)

    #Creating folder to hold zipped Jupyter Books
    os.mkdir(zippedJupyterBooks)

    #Creating folder to hold Jupyter Notebook HTML files
    os.mkdir(notebookHTMLS)

    #Creating folder to hold images for Notebook/Book Covers
    os.mkdir(jupyterImages)

    #Creating folder to hold Eswatini Repository
    os.mkdir(eswatiniRepository)

# Print out path names for testing
print("---------------------------------")
print('owd: ', owd, sep=None)
print('parentDirectory: ', parent_dir, sep=None)
print('jupyterDirectory: ', jupyterDirectory, sep=None)
print('jupyter: ', jupyter, sep=None)
print('jupyterBooks: ', jupyterBooks, sep=None)
print('jupyterNotebooks: ', jupyterNotebooks, sep=None)
print('zippedJupyterBooks: ', zippedJupyterBooks, sep=None)
print('eswatiniRepository: ', eswatiniRepository, sep=None)
print('eswatiniRepositoryNotebooks: ', eswatiniRepositoryNotebooks, sep=None)
print('eswatiniRepositoryBooks: ', eswatiniRepositoryBooks, sep=None)
print('eswatiniRepositoryZippedBooks: ', eswatiniRepositoryZippedBooks, sep=None)
print('eswatiniRepositoryImages: ', eswatiniRepositoryImages, sep=None)
print("---------------------------------")