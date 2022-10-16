#IMPORTS
from ast import main
from asyncio import subprocess
from configparser import ConfigParser
from genericpath import isfile
import json
import os
import pkg_resources
import shutil
import sys
import subprocess

###########################################################################################################
#Installing Dependencies
###########################################################################################################

required  = {'windows-curses', 'gitpython', 'jupyterlab', 'jupyter-book'} 
installed = {pkg.key for pkg in pkg_resources.working_set}
missing   = required - installed

if missing:
    # implement pip as a subprocess:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing])

import git
from git import repo

import curses
from curses import panel

###########################################################################################################
#Creating File Folder System
###########################################################################################################

parent_dir = os.path.expanduser('~')
parent_dir = parent_dir + "\OneDrive\Documents"
owd = os.getcwd() #original working directory

jupyterDirectory = os.path.join(parent_dir, "JupyterDirectory")
jupyter = os.path.join(jupyterDirectory, "Jupyter")
jupyterBooks = os.path.join(jupyter, "JupyterBooks")
jupyterNotebooks = os.path.join(jupyter, "JupyterNotebooks")
zippedJupyterBooks = os.path.join(jupyterBooks, "ZippedJupyterBooks")
eswatiniRepository = os.path.join(jupyterDirectory, "EswatiniRepository")
eswatiniRepositoryNotebooks = os.path.join(eswatiniRepository, "static", "books", "juypterNotebooks")
eswatiniRepositoryBooks = os.path.join(eswatiniRepository, "static", "books", "juypterBooks")
eswatiniRepositoryZippedBooks = os.path.join(eswatiniRepository, "static", "books", "zippedJuypterBooks")

#Print out path names for testing
# print("---------------------------------")
# print('owd: ', owd, sep=None)
# print('jupyterDirectory: ', jupyterDirectory, sep=None)
# print('jupyter: ', jupyter, sep=None)
# print('jupyterBooks: ', jupyterBooks, sep=None)
# print('jupyterNotebooks: ', jupyterNotebooks, sep=None)
# print('zippedJupyterBooks: ', zippedJupyterBooks, sep=None)
# print('eswatiniRepository: ', eswatiniRepository, sep=None)
# print('eswatiniRepositoryNotebooks: ', eswatiniRepositoryNotebooks, sep=None)
# print('eswatiniRepositoryBooks: ', eswatiniRepositoryBooks, sep=None)
# print('eswatiniRepositoryZippedBooks: ', eswatiniRepositoryZippedBooks, sep=None)
# print("---------------------------------")

if (os.path.exists(jupyterDirectory)) is False:

    print("Performing first time setup\n")
    print("A file system for storing your Jupyter Books and Notebooks, as well as the Eswatini Repository")
    print("will be created in your documents folder\n")
    print("Creating File Folder system...\n")

    ###########################################################################################################
    #Creating File Folder System
    ###########################################################################################################

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

    #Creating folder to hold Eswatini Repository
    os.mkdir(eswatiniRepository)

    ###########################################################################################################
    #Creating Config File
    ###########################################################################################################

    print("Creating configuration file...\n")

    os.chdir(jupyterDirectory)

    configObject = ConfigParser()

    configObject["USERINFO"] = {
        "username": "",
        "PAT": ""
    }

    configObject["FIRSTTIMESETUP"] = {
        "firstTimeSetup": "yes"
    }

    with open('config.ini', 'w') as conf:
        configObject.write(conf)

    os.chdir(owd)

    ###########################################################################################################
    #Installing GitPython
    ###########################################################################################################

    #print("Installing GitPython...\n")

    #pip.main(["install", "--user", "gitpython"])

    #print()

    ###########################################################################################################
    #Cloning Eswatini Repository
    ###########################################################################################################

    print("Cloning Eswatini repository...\n")

    git.Repo.clone_from('https://github.com/University-of-Eswatini/Eswatini-Project.git', eswatiniRepository)

    ###########################################################################################################
    #Installing Jupyter Labs and BooksInstalling Jupyter Labs and Books
    ###########################################################################################################

    #print("Installing Jupyter Labs...\n")
    #pip.main(["install", "--user", "jupyterlab"]) #os.system('cmd /k "py -m jupyterlab"') opens jupyter lab
    #print()

    #print("Installing Jupyter Books...\n")
    #pip.main(["install", "--user", "jupyter-book"]) #os.system('cmd /k "jb --help"') jupyter books
    #print()

    ###########################################################################################################
    #Installing GitHubs CLI commands
    ###########################################################################################################

    

else:

    print("First time set up already done.\n\n")

mainLoopConditional = True #True for staying in the loop, False for exiting the loop

while mainLoopConditional == True:

    mainMenuAnswer = True #True for staying in the loop, False for exiting the loop

    while mainMenuAnswer == True:

        print("-------------------------------------------------------------------------------\n")
        print("Main Menu")
        print("""
1)Open Jupyter Lab where you can create or edit Jupyter Notebooks
2)Create a new Jupyter Book
3)Upload a Jupyter Notebook or Book to the Eswatini textbook resource website
4)Options Menu
5)Exit
        """)

        mainMenuOption = ''

        try:
            mainMenuOption = int(input('Enter your choice: '))
            print()
            print("-------------------------------------------------------------------------------\n")
        except:
            print('Wrong input. Please enter a number.')

        if mainMenuOption == 1:
            mainMenuAnswer = False

        elif mainMenuOption == 2:
            mainMenuAnswer = False

        elif mainMenuOption == 3:
            mainMenuAnswer = False

        elif mainMenuOption == 4:
            mainMenuAnswer = False

        elif mainMenuOption == 5:
            mainMenuAnswer = False

        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

    ###########################################################################################################
    #1)Open Jupyter Lab where you can create or edit Jupyter Notebooks
    ###########################################################################################################

    if mainMenuOption == 1:

        print("Opening Jupyter Labs.")
        print("This will open in a new terminal.")
        print("This terminal will pause until you have closed the Jupyter Notebook Terminal.")
        print()
        print("-------------------------------------------------------------------------------")

        path = jupyter.replace("\\", "/")
        command = 'cmd /k "py -m jupyterlab --notebook-dir=' + path + '"'

        os.chdir(owd)
        subprocess.call(command, creationflags = subprocess.CREATE_NEW_CONSOLE)

        #Exit choice one menu

        choiceOneExitMenuAnswer = True

        print()
        print('Exit Menu')

        while choiceOneExitMenuAnswer == True:

            print("""
1)Return to Main Menu
2)Exit
            """)

            choiceOneExitMenuOption = ''

            try:
                choiceOneExitMenuOption = int(input('Enter your choice: '))
            except:
                print('Wrong input. Please enter a number.')

            if choiceOneExitMenuOption == 1:
                print()
                choiceOneExitMenuAnswer = False

            elif choiceOneExitMenuOption == 2:
                print()
                choiceOneExitMenuAnswer = False
                mainLoopConditional == False
                exit()

            else:
                print("Invalid choice. Please enter a number between 1 and 2.")

        
    ###########################################################################################################
    #2)Create a new Jupyter Book
    ###########################################################################################################

    elif mainMenuOption == 2:
        
        
        os.chdir(jupyterBooks)
        doesBookExist = True

        while doesBookExist is True:

            bookName = input("What is the name of your new Jupyter Book(Note that spaces will be removed): ")
            bookName = bookName.replace(" ","")
            bookName = bookName.replace("'", "")

            if os.path.exists(os.path.join(jupyterBooks, bookName)) is False:

                doesBookExist = False

                jbCommand = "jupyter-book create " + bookName

                os.chdir(jupyterBooks)
                subprocess.call(jbCommand)
            
            else:

                print("That book already exists, please either delete it or choose a different name\n")

        os.chdir(owd)

    ###########################################################################################################
    #3)Upload a Jupyter Notebook or Book to the Eswatini textbook resource website
    ###########################################################################################################

    elif mainMenuOption == 3:

        bookOrNotebookMenuAnswer = False

        while bookOrNotebookMenuAnswer == False:

            print("""
1)Jupyter Notebook
2)Jupyter Book
            """)

            bookOrNotebookMenuOption = ''

            try:
                bookOrNotebookMenuOption = int(input('Enter your choice: '))
            except:
                print('Wrong input. Please enter a number.')

            if bookOrNotebookMenuOption == 1:
                
                bookOrNotebookMenuAnswer = True

            elif bookOrNotebookMenuOption == 2:
                
                bookOrNotebookMenuAnswer = True

            else:

                print("Invalid choice. Please enter a number between 1 and 2.")


        if bookOrNotebookMenuOption == 1: #Uploading a Jupyter Notebook

            os.chdir(jupyterNotebooks)

            notebookFiles = []

            for x in os.listdir(): #Getting notebooks that exist in the users Notebook repository
                if x.endswith(".ipynb"):
                    notebookFiles.append(x)

            print('Which Jupyter Noteboook would you like to upload?\n')

            whichNotebookAnswer = False

            while whichNotebookAnswer == False: #Picking which notebook to upload

                for i in range(len(notebookFiles)):

                    print(i+1, ')', notebookFiles[i], sep=None)
                
                print()

                try:
                    whichNotebookOption = int(input('Enter your choice: '))
                except:
                    print('Wrong input. Please enter a number between 1 and ', len(notebookFiles), '.', sep=None)
                
                if whichNotebookOption > 0 and whichNotebookOption <= len(notebookFiles):

                    whichNotebookAnswer = True
                    notebookToBeUploaded = notebookFiles[whichNotebookOption-1]
                
                else:

                    print("Invalid choice. Please enter a number between 1 and ", len(notebookFiles), sep=None)
                    print()
                    print('Which Jupyter Noteboook would you like to upload?\n')
            
            os.chdir(eswatiniRepositoryNotebooks)

            if os.path.isfile(notebookToBeUploaded) == True:

                print()
                print("A Jupyter Notebook by that name already exists.")
                print("Please contact the website moderator to remove the book, or choose a different name for the book.")
                exitNotebook = 0

            
            else:
                
                os.chdir(jupyterNotebooks)
                shutil.copy(notebookToBeUploaded, eswatiniRepositoryNotebooks)
                exitNotebook = 1
            
            if exitNotebook == 1:

                os.chdir(eswatiniRepository)

                with open('textbooks.json', 'r') as openFile:

                    jsonObject = json.load(openFile)
                
                subjects = []

                print("Json file: ", jsonObject, sep=None)
                print()
                
                for i in jsonObject:

                    subjects.append(i)

                print(subjects)

        elif bookOrNotebookMenuOption == 2: #Uploading a Jupyter Book

            print('Jupyter Book')
        
        else:
            print('How did you get here?')
    ###########################################################################################################
    #4)Options Menu
    ###########################################################################################################

    elif mainMenuOption == 4:

        print("You chose 4")

    ###########################################################################################################
    #5)Exit
    ###########################################################################################################

    elif mainMenuOption == 5:

        print("Exiting...")
        exit()

    ###########################################################################################################
    #How did you get here?
    ###########################################################################################################

    else:

        print("How did you get here?")