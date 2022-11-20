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

###########################################################################################################
#Installing Dependencies
###########################################################################################################

required  = {'gitpython', 'jupyterlab', 'jupyter-book', 'nbconvert[webpdf]'} 
installed = {pkg.key for pkg in pkg_resources.working_set}
missing   = required - installed

if missing:
    #implementing pip as a subprocess:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing])

#Githubs CLI must be installed with Scoop
#Installing Scoop
subprocess.run(["powershell", "Set-ExecutionPolicy RemoteSigned -scope CurrentUser"])
subprocess.run(["powershell", "-Command", "iwr -useb get.scoop.sh | iex"])

import git
from git import repo

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
notebookHTMLS = os.path.join(jupyterNotebooks, "NotebookHTMLs")
zippedJupyterBooks = os.path.join(jupyterBooks, "ZippedJupyterBooks")
jupyterImages = os.path.join(jupyter, "JupyterImages")
eswatiniRepository = os.path.join(jupyterDirectory, "EswatiniRepository")
eswatiniRepositoryNotebooks = os.path.join(eswatiniRepository, "static", "books", "juypterNotebooks")
eswatiniRepositoryBooks = os.path.join(eswatiniRepository, "static", "books", "juypterBooks")
eswatiniRepositoryZippedBooks = os.path.join(eswatiniRepository, "static", "books", "zippedJuypterBooks")

#Print out path names for testing
# print("---------------------------------")
# print('owd: ', owd, sep=None)
# print('parentDirectory: ', parent_dir, sep=None)
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

    #Creating folder to hold Jupyter Notebook HTML files
    os.mkdir(notebookHTMLS)

    #Creating folder to hold images for Notebook/Book Covers
    os.mkdir(jupyterImages)

    #Creating folder to hold Eswatini Repository
    os.mkdir(eswatiniRepository)

    print()
    print('File Folder system created!\n')

    ###########################################################################################################
    #Installing GitHubs CLI
    ###########################################################################################################

    os.chdir(jupyterDirectory)
    bat = open(r'installGhCli.ps1', 'w+')
    bat.write("scoop install gh")
    bat.close()
    
    p = subprocess.Popen(["powershell.exe", os.path.join(jupyterDirectory, "installGhCli.ps1")], stdout=sys.stdout)
    p.communicate()
    os.remove(os.path.join(jupyterDirectory, "installGhCli.ps1"))
    os.chdir(owd)

    ###########################################################################################################
    #Creating Config File
    ###########################################################################################################

    print("Creating configuration file...\n")

    os.chdir(jupyterDirectory)

    print("In order to clone the Eswatini repository, you will need a Github Account along with your username and Personal Access Token (PAT)\n")
    print("You can generate a PAT by going to:")
    print("1. Github Account Settings (Click on your profile icon in top right corner of github and select settings at the bottom of the menu that pops up)")
    print("2. Developer Settings (Found at the bottom of the list of options on the left hand side of the page)")
    print("3. Personal Access Tokens (Found at the bottom of the list of options on the left hand side of the page)")
    print("4. Generate New Token (Found center-right near the top of the page)")
    print("5. Give your PAT a descriptive name, set the expiration date to be 'No Expiration' and check off 'REPO', 'WRITE:PACKAGES', 'USER', and 'READ:ORG' (found under ADMIN:ORG)")
    print("6. Select Generate Token at the bottom of your page and copy the token into your clip board\n")

    username = input("Enter your GitHub username: ")
    email = input("Enter your email associated with your Github account: ")
    personalAccessToken = input("Enter your Personal Access Token: ")
    
    configObject = ConfigParser()

    configObject.add_section('USERINFO')
    configObject.set('USERINFO', 'username', username)
    configObject.set('USERINFO', 'email', email)
    configObject.set('USERINFO', 'PAT', personalAccessToken)
    print()

    with open('config.ini', 'w') as conf:
        configObject.write(conf)

    os.chdir(owd)

    ###########################################################################################################
    #Logging User into Github using CLI
    ###########################################################################################################
    
    print("Logging into GitHub...\n")

    loggedOutMessage = (None, b'You are not logged into any GitHub hosts. Run \x1b[0;1;39mgh auth login\x1b[0m to authenticate.\n')

    checkStatus = subprocess.Popen(["powershell", "gh auth status"], stderr=subprocess.PIPE)
    checkStatusOutput = checkStatus.communicate()

    if checkStatusOutput == loggedOutMessage:

        os.chdir(jupyterDirectory)

        configOb = ConfigParser()
        configOb.read('config.ini')
        userInfo = configOb['USERINFO']
        tempUsername = userInfo['username']
        tempEmail = userInfo['email']
        tempPat = userInfo['PAT']

        print('Here is your username:', tempUsername, sep=None)
        print('Here is your email:', tempEmail, sep=None)
        print('Here is your PAT:', tempPat, sep=None)
        print()
        print("Please login using: 1. GitHub.com")
        print("                    2. HTTPS")
        print("                    3.Paste an authentication token")
        print()
        print("Then please paste your PAT and press enter.")
        print()

        subprocess.run(["powershell", "gh auth login"])

        os.chdir(owd)
    
    else:

        subprocess.run(["powershell", "gh auth status"])

    ###########################################################################################################
    #Cloning Eswatini Repository
    ###########################################################################################################

    print("Cloning Eswatini repository...\n")

    git.Repo.clone_from('https://github.com/University-of-Eswatini/Eswatini-Project.git', eswatiniRepository)

###########################################################################################################
#First Time Setup Already Done
###########################################################################################################

else:

    print("First time set up already done.\n\n")
    print("Logging into GitHub...\n")

    ###########################################################################################################
    #Logging User into Github
    ###########################################################################################################
    
    loggedOutMessage = (None, b'You are not logged into any GitHub hosts. Run \x1b[0;1;39mgh auth login\x1b[0m to authenticate.\n')

    checkStatus = subprocess.Popen(["powershell", "gh auth status"], stderr=subprocess.PIPE)
    checkStatusOutput = checkStatus.communicate()

    if checkStatusOutput == loggedOutMessage:

        os.chdir(jupyterDirectory)

        configOb = ConfigParser()
        configOb.read('config.ini')
        userInfo = configOb['USERINFO']
        tempUsername = userInfo['username']
        tempEmail = userInfo['email']
        tempPat = userInfo['PAT']

        print('Here is your username:', tempUsername, sep=None)
        print('Here is your email:', tempEmail, sep=None)
        print('Here is your PAT:', tempPat, sep=None)
        print()

        subprocess.run(["powershell", "gh auth login"])

        os.chdir(owd)
    
    else:

        subprocess.run(["powershell", "gh auth status"])

    ###########################################################################################################
    #Updating Repository
    ###########################################################################################################

    os.chdir(eswatiniRepository)

    gitPullUpdate = subprocess.Popen(['git', 'pull'])
    gitPullUpdate.communicate()

    os.chdir(owd)

###########################################################################################################
#PROGRAM MAIN MENU LOOP
###########################################################################################################

#Main Menu Loop#

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
5)Help
6)Exit
        """)

        mainMenuOption = ''

        try:
            mainMenuOption = int(input('Enter your choice: '))
            print()
            print("-------------------------------------------------------------------------------\n")
        except:
            print('Wrong input. Please enter a number.')

        #Open Jupyter Lab where you can create or edit Jupyter Notebooks
        if mainMenuOption == 1:
            mainMenuAnswer = False

        #Create a new Jupyter Book
        elif mainMenuOption == 2:
            mainMenuAnswer = False

        #Upload a Jupyter Notebook or Book to the Eswatini textbook resource website
        elif mainMenuOption == 3:
            mainMenuAnswer = False

        #Options Menu
        elif mainMenuOption == 4:
            mainMenuAnswer = False

        #Help
        elif mainMenuOption == 5:
            mainMenuAnswer = False
            
        #Exit
        elif mainMenuOption == 6:
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
        subprocess.call(command, creationflags = subprocess.CREATE_NEW_CONSOLE) #Opens jupyter lab in a new terminal

        #Exit choice one menu

        print()
        print('Exit Menu')

        choiceOneExitMenuAnswer = True #True for staying in the loop, False for exiting the loop

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

            #Return to Main Menu
            if choiceOneExitMenuOption == 1:

                print()
                choiceOneExitMenuAnswer = False

            #Exit
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

        doesBookExist = True #True for staying in the loop, False for exiting the loop

        while doesBookExist is True: 

            bookName = input("What is the name of your new Jupyter Book(Note that spaces will be removed): ")
            bookName = bookName.replace(" ","")
            bookName = bookName.replace("'", "")

            if os.path.exists(os.path.join(jupyterBooks, bookName)) is False: #If user doesn't already have a book by that name in their own repository

                doesBookExist = False

                #Creating a new jupyter book with the given name
                jbCommand = "jupyter-book create " + bookName
                os.chdir(jupyterBooks)
                subprocess.call(jbCommand)
            
            else:

                print("That book already exists, please either delete it or choose a different name\n")

        os.chdir(owd)

    ###########################################################################################################
    #3)Upload a Jupyter Notebook or Book to the Eswatini textbook resource website
    ###########################################################################################################

    #Choosing either a Jupyter Book or Notebook Loop

    elif mainMenuOption == 3:

        bookOrNotebookMenuAnswer = True #True for staying in the loop, False for exiting the loop

        while bookOrNotebookMenuAnswer == True:

            print("""
1)Jupyter Notebook
2)Jupyter Book
            """)

            bookOrNotebookMenuOption = ''

            try:
                bookOrNotebookMenuOption = int(input('Enter your choice: '))
            except:
                print('Wrong input. Please enter a number.')

            #Jupyter Notebook
            if bookOrNotebookMenuOption == 1:
                
                bookOrNotebookMenuAnswer = False

            #Jupyter Book
            elif bookOrNotebookMenuOption == 2:
                
                bookOrNotebookMenuAnswer = False

            else:

                print("Invalid choice. Please enter a number between 1 and 2.")

        #Uploading a Jupyter Notebook

        if bookOrNotebookMenuOption == 1: 

            os.chdir(jupyterNotebooks)

            existingNotebooks = [] #Will hold all the notebooks stored in the users directory

            #Variables to be written into the textbooks.json file
            notebookAuthor = ''
            notebookClass = ''
            notebookDescription = ''
            notebookFile = ''
            notebookImage = ''
            notebookName = ''
            notebookSubject = '' 
            notebookZip = '' #Should always be '' for notebooks
            
           #Picking which notebook to upload

            for x in os.listdir(): #Getting notebooks that exist in the users Notebook repository
                if x.endswith(".ipynb"):
                    existingNotebooks.append(x)

            print('Which Jupyter Notebook would you like to upload?\n')

            whichNotebookAnswer = True #True for staying in the loop, False for exiting the loop

            while whichNotebookAnswer == True: 

                for i in range(len(existingNotebooks)):

                    print(i+1, ')', existingNotebooks[i], sep=None)
                
                print()

                try:
                    whichNotebookOption = int(input('Enter your choice: '))
                except:
                    print('Wrong input. Please enter a number between 1 and ', len(existingNotebooks), '.', sep=None)
                
                if whichNotebookOption > 0 and whichNotebookOption <= len(existingNotebooks):

                    whichNotebookAnswer = False
                    notebookToBeUploaded = existingNotebooks[whichNotebookOption-1]
                
                else:

                    print("Invalid choice. Please enter a number between 1 and ", len(existingNotebooks), sep=None)
                    print()
                    print('Which Jupyter Noteboook would you like to upload?\n')
            
            os.chdir(eswatiniRepositoryNotebooks)

            #Checking if that notebook name already exists

            if os.path.isfile(notebookToBeUploaded) == True: #Stops user from uploading a Notebook thats name already exists
                                                             #Prevents pathing issues on the website
                print()
                print("A Jupyter Notebook by that name already exists.")
                print("Please contact the website moderator to remove the Notebook, or choose a different name for the book.")
                exitNotebook = 0 #Causes the program to skip back to the main menu
            
            else:
                
                #Copying 'notebook to be uploaded' into the HTML folder and creating an HTML version then removing 'notebook to be uploaded' from the HTML folder

                os.chdir(jupyterNotebooks)
                shutil.copy(notebookToBeUploaded, eswatiniRepositoryNotebooks)
                shutil.copy(notebookToBeUploaded, notebookHTMLS)

                os.chdir(notebookHTMLS)
                convertNotebookToPDF = subprocess.Popen(['jupyter', 'nbconvert', '--to', 'HTML', notebookToBeUploaded])
                convertNotebookToPDF.communicate()
                os.remove(notebookToBeUploaded)
                os.chdir(owd)

                #Creating the path the website will use
                notebookFile = "books/juypterNotebooks/" + notebookToBeUploaded
                exitNotebook = 1
            
            if exitNotebook == 1: #Book did not already exist and the user wishes to upload it

                os.chdir(eswatiniRepository)

                #Appending the top level keys from textbooks.json into an array (ie: the subjects available to be uploaded to)
                with open('textbooks.json', 'r') as openFile:

                    jsonFile = json.load(openFile)
                    openFile.close()
                
                subjects = []
                
                for i in jsonFile: #Getting subjects from json file

                    subjects.append(i)

                print()
                print('Which subject does this Jupyter Notebook belong in?\n')
        
                #Picking which subject the Notebook belongs to

                whichNotebookSubjectAnswer = True #True for staying in the loop, False for exiting the loop

                while whichNotebookSubjectAnswer == True:

                    for i in range(len(subjects)):

                        print(i+1, ')', subjects[i], sep=None)
                    
                    print()

                    try:
                        whichNotebookSubjectOption = int(input('Enter your choice: '))
                    except:
                        print('Wrong input. Please enter a number between 1 and ', len(subjects), '.', sep=None)
                    
                    if whichNotebookSubjectOption > 0 and whichNotebookSubjectOption <= len(subjects):

                        whichNotebookSubjectAnswer = False
                        notebookSubject = subjects[whichNotebookSubjectOption-1]
                    
                    else:

                        print("Invalid choice. Please enter a number between 1 and ", len(subjects), sep=None)
                        print()
                        print('Which subject does this Jupyter Notebook belong in?\n')

                #Getting pertinant information from the user and saving to variables that will be written to textbooks.json
                print()
                notebookName = input("What is this Notebooks title: ")
                print()
                notebookClass = input("What class is this Notebook for: ")
                print()
                notebookAuthor = input("Who is the author of this Notebook: ")
                print()
                notebookDescription = input("Please enter a short description of your Notebook: ")
                print()
                
                # Testing to make sure input is saved correctly
                # print()
                # print('Name:', notebookName, sep=None)
                # print('Class:', notebookClass, sep=None)
                # print('Author:', notebookAuthor, sep=None)
                # print('Description:', notebookDescription, sep=None)
                # print('File:', notebookFile, sep=None)
                # print('File:', 'books/juypterNotebooks/teset.ipynb', sep=None)

                #Writing notebook data to json file

                jsonData = {
                    "file": notebookFile,
                    "zip": "",
                    "type": "notebook",
                    "name": notebookName,
                    "descript": notebookDescription,
                    "author": notebookAuthor,
                    "class": notebookClass,
                    "image": ""
                }

                jsonFile[notebookSubject].append(jsonData)
                jsonOutFile = open("textbooks.json", "w")
                json.dump(jsonFile, jsonOutFile, indent=3)
                jsonOutFile.close()

                os.chdir(jupyterDirectory)

                #Getting users GitHub username to add to pull request title
                configOb = ConfigParser()
                configOb.read('config.ini')
                userInfo = configOb['USERINFO']
                tempUsername = userInfo['username']

                os.chdir(eswatiniRepository)

                branchName = input("Enter a name for your pull requests branch: ")
                branchName = branchName.replace(" ","")
                branchName = branchName.replace("'", "")
                branchName = branchName.replace("-", "")

                #Stashing local changes
                gitStash = subprocess.Popen(['git', 'stash'])
                gitStash.communicate()

                #Creating new branch for pull request
                gitMakeNewBranch = subprocess.Popen(['git', 'branch', branchName])
                gitMakeNewBranch.communicate()

                #Updating local repository before commiting changes
                gitUpdate= subprocess.Popen(['git', 'pull'])
                gitUpdate.communicate()

                #Applying stashed local changes
                gitStashApply = subprocess.Popen(['git', 'stash', 'apply'])
                gitStashApply.communicate()

                #Checking out new branch for pull request
                gitCheckOutNewBranch = subprocess.Popen(['git', 'checkout', branchName])
                gitCheckOutNewBranch.communicate()

                #Git adding all changes to be commited
                gitAdd = subprocess.Popen(['git', 'add', '.'])
                gitAdd.communicate()

                #Commiting local changes
                gitCommit = subprocess.Popen(['git', 'commit', '-m"Pull request for new Jupyter Notebook for ' + tempUsername + '"'])
                gitCommit.communicate()

                print()
                print("-----------------------------------------------------------------------------------------------------")
                print("The program will now create a pull request to the Eswatini Repository")
                print("Please select the first option 'University-of-Eswatini/Eswatini-Project'")
                print("The program will then generate a title for your pull request with your username. Please press enter.")
                print("If you then wish to add comments you can do so by pressing 'e'. Press enter to skip.")
                print("Finally select the first option 'Submit' to submit your pull request.")
                print("-----------------------------------------------------------------------------------------------------")
                print()

                #Creating pull request for commited changes
                ghPullRequest = subprocess.Popen(['gh', 'pr', 'create'])
                ghPullRequest.communicate()

                #Checking out the main branch
                gitCheckOutMain = subprocess.Popen(['git', 'checkout', 'main'])
                gitCheckOutMain.communicate()

                #Deleting pull request branch to keep local repository up to date and prventing branch bloat
                gitDeleteBranch = subprocess.Popen(['git', 'branch', '-D', branchName])
                gitDeleteBranch.communicate()

                print()
                print()

        #Uploading a Jupyter Book

        elif bookOrNotebookMenuOption == 2:

            os.chdir(jupyterBooks)

            existingBooks = [] #Will hold all the notebooks stored in the users directory

            #Variables to be written into the textbooks.json file
            bookAuthor = ''
            bookClass = ''
            bookDescription = ''
            bookFile = ''
            bookImage = ''
            bookName = ''
            bookSubject = ''
            bookType = 'book' #Must always be 'book' for notebooks
            bookZip = ''

            #Picking which notebook to upload

            for x in os.listdir(): #Getting notebooks that exist in the users Notebook repository
                if x == "ZippedJupyterBooks":
                    continue
                else:
                    existingBooks.append(x)

            print('Which Jupyter Book would you like to upload?\n')

            whichBookAnswer = True #True for staying in the loop, False for exiting the loop

            while whichBookAnswer == True: 

                for i in range(len(existingBooks)):

                    print(i+1, ')', existingBooks[i], sep=None)
                
                print()

                try:
                    whichBookOption = int(input('Enter your choice: '))
                except:
                    print('Wrong input. Please enter a number between 1 and ', len(existingBooks), '.', sep=None)
                
                if whichBookOption > 0 and whichBookOption <= len(existingBooks):

                    whichBookAnswer = False
                    bookToBeUploaded = existingBooks[whichBookOption-1]
                
                else:

                    print("Invalid choice. Please enter a number between 1 and ", len(existingBooks), sep=None)
                    print()
                    print('Which Jupyter Book would you like to upload?\n')
            
            os.chdir(eswatiniRepositoryBooks)

            #Checking if that notebook name already exists

            if os.path.isdir(bookToBeUploaded) == True: #Stops user from uploading a Book thats name already exists
                                                        #Prevents pathing issues on the website
                print()
                print("A Jupyter Book by that name already exists.")
                print("Please contact the website moderator to remove the book, or choose a different name for the book.")
                exitBook = 0
            
            else:
                
                os.chdir(jupyterBooks)

                print("Building Jupyer Book...\n")

                #Building HTML version of the Book to be uploaded
                buildBook = subprocess.Popen(['jupyter-book', 'build', bookToBeUploaded])
                buildBook.communicate()

                #Copying book into the correct folder in eswatini repository
                tempBookPath = os.path.join(eswatiniRepositoryBooks, bookToBeUploaded)
                shutil.copytree(bookToBeUploaded, tempBookPath)

                #Copying book to the zipped books folder to be zipped
                tempBookPath = os.path.join(zippedJupyterBooks, bookToBeUploaded)
                shutil.copytree(bookToBeUploaded, tempBookPath)

                #Zipping the Book to be uploaded and removing the unzipped version
                os.chdir(zippedJupyterBooks)
                make_archive(bookToBeUploaded, "zip")
                shutil.rmtree(tempBookPath)

                #Copying Zipped Book to be uploaded to the correct folder in eswatini repository
                zippedBook = bookToBeUploaded + ".zip"
                tempBookPath = os.path.join(eswatiniRepositoryZippedBooks, zippedBook)
                shutil.copy(zippedBook, eswatiniRepositoryZippedBooks)

                #Creating the path(s) for zipped and unzipped books that the website will use
                bookFile = "books/juypterBooks/" + bookToBeUploaded + "/_build/html/index.html"
                zippedBookFile = "books/zippedJuypterBooks/" + bookToBeUploaded + ".zip"
                exitBook = 1

            if exitBook == 1: #Book did not already exist and the user wishes to upload it

                os.chdir(eswatiniRepository)

                #Appending the top level keys from textbooks.json into an array (ie: the subjects available to be uploaded to)
                with open('textbooks.json', 'r') as openFile:

                    jsonFile = json.load(openFile)
                    openFile.close()
                    
                subjects = []
                    
                for i in jsonFile: #Getting subjects from json file

                    subjects.append(i)

                print()
                print('Which subject does this Jupyter Book belong in?\n')

                #Picking which subject the Book belongs to

                whichBookSubjectAnswer = True #True for staying in the loop, False for exiting the loop

                while whichBookSubjectAnswer == True:

                    for i in range(len(subjects)):

                        print(i+1, ')', subjects[i], sep=None)
                        
                    print()

                    try:
                        whichBookSubjectOption = int(input('Enter your choice: '))
                    except:
                        print('Wrong input. Please enter a number between 1 and ', len(subjects), '.', sep=None)
                        
                    if whichBookSubjectOption > 0 and whichBookSubjectOption <= len(subjects):

                        whichBookSubjectAnswer = False
                        bookSubject = subjects[whichBookSubjectOption-1]
                        
                    else:

                        print("Invalid choice. Please enter a number between 1 and ", len(subjects), sep=None)
                        print()
                        print('Which subject does this Jupyter Book belong in?\n')

                #Getting pertinant information from the user and saving to variables that will be written to textbooks.json
                print()
                bookName = input("What is this Notebooks title: ")
                print()
                bookClass = input("What class is this Notebook for: ")
                print()
                bookAuthor = input("Who is the author of this Notebook: ")
                print()
                bookDescription = input("Please enter a short description of your Notebook: ")
                print()
                
                #Testing to make sure input is saved correctly
                # print()
                # print('Name:', bookName, sep=None)
                # print('Class:', bookClass, sep=None)
                # print('Author:', bookAuthor, sep=None)
                # print('Description:', bookDescription, sep=None)
                # print('Subject:', bookSubject, sep=None)
                # print('File:', bookFile, sep=None)
                # print('Zip:', zippedBookFile, sep=None)

                #Writing notebook data to json file

                jsonData = {
                    "file": bookFile,
                    "zip": zippedBookFile,
                    "type": "book",
                    "name": bookName,
                    "descript": bookDescription,
                    "author": bookAuthor,
                    "class": bookClass,
                    "image": ""
                }

                jsonFile[bookSubject].append(jsonData)
                jsonOutFile = open("textbooks.json", "w")
                json.dump(jsonFile, jsonOutFile, indent=3)
                jsonOutFile.close()

                os.chdir(jupyterDirectory)

                #Getting users GitHub username to add to pull request title
                configOb = ConfigParser()
                configOb.read('config.ini')
                userInfo = configOb['USERINFO']
                tempUsername = userInfo['username']

                os.chdir(eswatiniRepository)

                branchName = input("Enter a name for your pull requests branch: ")
                branchName = branchName.replace(" ","")
                branchName = branchName.replace("'", "")
                branchName = branchName.replace("-", "")

                #Stashing local changes
                gitStash = subprocess.Popen(['git', 'stash'])
                gitStash.communicate()

                #Creating new branch for pull request
                gitMakeNewBranch = subprocess.Popen(['git', 'branch', branchName])
                gitMakeNewBranch.communicate()

                #Updating local repository before commiting changes
                gitUpdate= subprocess.Popen(['git', 'pull'])
                gitUpdate.communicate()

                #Applying stashed local changes
                gitStashApply = subprocess.Popen(['git', 'stash', 'apply'])
                gitStashApply.communicate()

                #Checking out new branch for pull request
                gitCheckOutNewBranch = subprocess.Popen(['git', 'checkout', branchName])
                gitCheckOutNewBranch.communicate()

                #Git adding all changes to be commited
                gitAdd = subprocess.Popen(['git', 'add', '.'])
                gitAdd.communicate()

                #Commiting local changes
                gitCommit = subprocess.Popen(['git', 'commit', '-m"Pull request for new Jupyter Book for ' + tempUsername + '"'])
                gitCommit.communicate()

                print()
                print("-----------------------------------------------------------------------------------------------------")
                print("The program will now create a pull request to the Eswatini Repository")
                print("Please select the first option 'University-of-Eswatini/Eswatini-Project'")
                print("The program will then generate a title for your pull request with your username. Please press enter.")
                print("If you then wish to add comments you can do so by pressing 'e'. Press enter to skip.")
                print("Finally select the first option 'Submit' to submit your pull request.")
                print("-----------------------------------------------------------------------------------------------------")
                print()

                #Creating pull request for commited changes
                ghPullRequest = subprocess.Popen(['gh', 'pr', 'create'])
                ghPullRequest.communicate()

                #Checking out the main branch
                gitCheckOutMain = subprocess.Popen(['git', 'checkout', 'main'])
                gitCheckOutMain.communicate()

                #Deleting pull request branch to keep local repository up to date and prventing branch bloat
                gitDeleteBranch = subprocess.Popen(['git', 'branch', '-D', branchName])
                gitDeleteBranch.communicate()

                print()
                print()
        
        else:
            print('How did you get here?')

    ###########################################################################################################
    #4)Options Menu
    ###########################################################################################################

    elif mainMenuOption == 4:

        optionsMenuLoop = True #True for staying in the loop, False for exiting the loop

        while optionsMenuLoop == True:

            optionsMenuAnswer = True #True for staying in the loop, False for exiting the loop

            while optionsMenuAnswer == True:
                print("-------------------------------------------------------------------------------\n")
                print("Options Menu")
                print("""
1)Update your Eswatini Repository (Git Pull)
2)Update your GitHub credentials (Username / Email / Personal Access Token)
3)Log out of GitHub
4)Log into GitHub
5)Exit to Main Menu
                """)

                optionsMenuOption = ''

                try:
                    optionsMenuOption = int(input('Enter your choice: '))
                except:
                    print('Invalid choice. Please enter a number between 1 and 5.')

                #Update your Eswatini Repository (Git Pull)
                if optionsMenuOption == 1:

                    print()
                    optionsMenuAnswer = False

                #Update your GitHub credentials (Username / Email / Personal Access Token)
                elif optionsMenuOption == 2:

                    print()
                    optionsMenuAnswer = False

                #Log out of GitHub
                elif optionsMenuOption == 3:

                    print()
                    optionsMenuAnswer = False

                #Log into GitHub
                elif optionsMenuOption == 4:

                    print()
                    optionsMenuAnswer = False
                
                #Exit to Main Menu
                elif optionsMenuOption == 5:

                    print()
                    optionsMenuAnswer = False

                else:
                    print("Invalid choice. Please enter a number between 1 and 5.")

            #Update your Eswatini Repository (Git Pull)
            if optionsMenuOption == 1:

                os.chdir(eswatiniRepository)

                gitPullUpdate = subprocess.Popen(['git', 'pull'])
                gitPullUpdate.communicate()

                os.chdir(owd)

            #Update your GitHub credentials (Username / Email / Personal Access Token)
            if optionsMenuOption == 2:

                os.chdir(jupyterDirectory)

                configOb = ConfigParser()
                configOb.read('config.ini')
                userInfo = configOb['USERINFO']
                tempUsername = userInfo['username']
                tempEmail = userInfo['email']
                tempPat = userInfo['PAT']

                print('Here is your current username:', tempUsername, sep=None)
                print('Here is your current email:', tempEmail, sep=None)
                print('Here is your current PAT:', tempPat, sep=None)
                print()
                print("You can copy paste any information from here that you do not wish to change.")
                print()

                tempUsername = input("Enter your new GitHub username: ")
                tempEmail = input("Enter your new email associated with your Github account: ")
                tempPat = input("Enter your new Personal Access Token: ")

                configOb.set('USERINFO', 'username', tempUsername)
                configOb.set('USERINFO', 'email', tempEmail)
                configOb.set('USERINFO', 'PAT', tempPat)
                print()

                with open('config.ini', 'w') as conf:
                    configOb.write(conf)

                print("Github Credentials updated.")

                os.chdir(owd)

            #Log out of GitHub
            if optionsMenuOption == 3:

                subprocess.run(["powershell", "gh auth logout"])

            #Log into GitHub
            if optionsMenuOption == 4:

                loggedOutMessage = (None, b'You are not logged into any GitHub hosts. Run \x1b[0;1;39mgh auth login\x1b[0m to authenticate.\n')

                checkStatus = subprocess.Popen(["powershell", "gh auth status"], stderr=subprocess.PIPE)
                checkStatusOutput = checkStatus.communicate()

                if checkStatusOutput == loggedOutMessage:

                    os.chdir(jupyterDirectory)

                    configOb = ConfigParser()
                    configOb.read('config.ini')
                    userInfo = configOb['USERINFO']
                    tempUsername = userInfo['username']
                    tempEmail = userInfo['email']
                    tempPat = userInfo['PAT']

                    print('Here is your username:', tempUsername, sep=None)
                    print('Here is your email:', tempEmail, sep=None)
                    print('Here is your PAT:', tempPat, sep=None)
                    print()
                    print("Please login using GitHub.com, HTTPS, and by Pasting an Authentication Token (found above)")
                    print()

                    subprocess.run(["powershell", "gh auth login"])

                    os.chdir(owd)
                
                else:

                    subprocess.run(["powershell", "gh auth status"])

                    print()
                    print("You are already logged in. Please logout first before logging in as a new user.")

            #Exit to Main Menu
            if optionsMenuOption == 5:

                print("Exiting to Main Menu.")
                optionsMenuLoop = False

    ###########################################################################################################
    #5)Help
    ###########################################################################################################

    elif mainMenuOption == 5:

        print("This program was created to help upload Jupyter Notebooks and Books to the Eswatini Textbook website\n")
        print("There are several key things to note when using this program:\n")
        print("    1) Any Jupyter Books or Notebooks should be kept in the respective folders created by the program, otherwise they will not be available to be selected to be uploaded.")
        print("       This is also true for images you would like to use for the Jupyter Notebooks or Books cover.\n")
        print("    2) These folders can be found by navigating to your 'Documents' folder in the file explorer and entering the 'JupyterDirectory' folder.\n")
        tempEnterToExitHelp = input("Press ENTER to return to the main menu")
    
    ###########################################################################################################
    #5)Exit
    ###########################################################################################################

    elif mainMenuOption == 6:

        print("Exiting...")
        exit()

    ###########################################################################################################
    #How did you get here?
    ###########################################################################################################

    else:

        print("How did you get here?")