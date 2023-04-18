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
from subprocess import STDOUT, DEVNULL
import cutie
from datetime import datetime

###########################################################################################################
#Functions
###########################################################################################################

def createPaths():

    """createPaths:
        
        Determines whether the user has OneDrice in their path or not and creates paths
        for file folders for the users repository"""

    global parent_dir

    global jupyterDirectory
    global jupyter
    global jupyterBooks
    global jupyterNotebooks
    global notebookHTMLS
    global zippedJupyterBooks
    global jupyterImages

    #Eswatini Repository Paths
    global eswatiniRepository
    global eswatiniRepositoryNotebooks
    global eswatiniRepositoryHTML
    global eswatiniRepositoryBooks
    global eswatiniRepositoryZippedBooks 
    global eswatiniRepositoryImages

    #Creating Paths Names for repository

    if os.path.isdir(parent_dir + "OneDrive\Documents"): #The user has OneDrive in their path

        parent_dir = parent_dir + "OneDrive\Documents"

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

    elif os.path.isdir(parent_dir + "\Documents"): #The user does not have OneDrive in their path
        
        parent_dir = parent_dir + "\Documents"

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

    else:
        print('Unable to create the file folder system.')
        print('Exiting...')
        quit()

def createFileFolders():

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

    print('File Folder system created!\n')

def createConfigFile():

    print("Creating configuration file...\n")

    os.chdir(jupyterDirectory)

    print("In order to clone the Eswatini repository, you will need a Github Account along with your username and Personal Access Token (PAT)\n")
    print("You can generate a PAT by going to:")
    print("1. Github Account Settings (Click on your profile icon in top right corner of github and select settings at the bottom of the menu that pops up)")
    print("2. Developer Settings (Found at the bottom of the list of options on the left hand side of the page)")
    print("3. Personal Access Tokens (Found at the bottom of the list of options on the left hand side of the page)")
    print("4. Generate New Token (Found center-right near the top of the page)")
    print("5. Give your PAT a descriptive name, set the expiration date to be 'No Expiration' and check off 'REPO', 'WRITE:PACKAGES', 'USER', and 'READ:ORG' (found under ADMIN:ORG)")
    print("6. Select Generate Token at the bottom of your page and copy the token into your clip board")
    print("       |-> It is good practice to also copy your PAT to a notepad file as it is unrecoverable from GitHub after leaving the page\n")

    username = input("Enter your GitHub username: ")
    email = input("Enter your email associated with your Github account: ")
    personalAccessToken = input("Enter your Personal Access Token: ")
    
    configObject = ConfigParser()

    configObject.add_section('USERINFO')
    configObject.set('USERINFO', 'username', username)
    configObject.set('USERINFO', 'email', email)
    configObject.set('USERINFO', 'PAT', personalAccessToken)
    configObject.set('USERINFO', 'branch', '')
    configObject.set('USERINFO', 'book', '')
    print()

    with open('config.ini', 'w') as conf:
        configObject.write(conf)

    os.chdir(owd)

def logIntoGitHub():

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
        print("                    3. Paste an authentication token")
        print()
        print("Then please paste your PAT and press enter.")
        print()

        subprocess.run(["powershell", "gh auth login"])

        os.chdir(owd)
    
    else:

        subprocess.run(["powershell", "gh auth status"])

        print("\nIf this is not you, you can log out and back in in the options menu.\n")

def cloneRepository():

    print("Cloning Eswatini repository...\n")

    gitClone = subprocess.Popen(['git', 'clone', 'https://github.com/University-of-Eswatini/Eswatini-Project.git', eswatiniRepository])
    gitClone.communicate()

def setGitConfig():

    print()
    print('Setting git config settings...\n')

    os.chdir(jupyterDirectory)

    gitConfigOb = ConfigParser()
    gitConfigOb.read('config.ini')
    gitUserInfo = gitConfigOb['USERINFO']
    gitUsername = gitUserInfo['username']
    gitEmail = gitUserInfo['email']

    gitConfigUsername = subprocess.Popen(['git', 'config', '--global', 'user.name', gitUsername])
    gitConfigUsername.communicate()

    gitConfigEmail = subprocess.Popen(['git', 'config', '--global', 'user.email', gitEmail])
    gitConfigEmail.communicate()

    print('Git config settings set!\n')

def updateRepository():

    print('Updating Eswatini Repository\n')

    os.chdir(jupyterDirectory)

    configOb = ConfigParser()
    configOb.read('config.ini')
    userInfo = configOb['USERINFO']
    tempPat = userInfo['PAT']

    gitAuth = "https://[{}]@github.com/University-of-Eswatini/Eswatini-Project.git".format(tempPat)

    os.chdir(eswatiniRepository)

    #gitRemoteSet = subprocess.Popen(['git', 'remote', 'set-url', 'origin', gitAuth])

    gitPullUpdate = subprocess.Popen(['git', 'pull', gitAuth])
    
    gitPullUpdate.communicate()

    os.chdir(owd)

def deleteBranch():

    os.chdir(jupyterDirectory)

    configOb = ConfigParser()
    configOb.read('config.ini')
    userInfo = configOb['USERINFO']
    branch = userInfo['branch']
    book = userInfo['book']

    if branch != '':

        os.chdir(eswatiniRepository)

        gitFetch = subprocess.Popen(['git', 'fetch'])
        gitFetch.communicate()

        gitStash = subprocess.Popen(['git', 'stash'])
        gitStash.communicate()

        gitStashDrop = subprocess.Popen(['git', 'stash', 'drop'])
        gitStashDrop.communicate()

        gitClean = subprocess.Popen(['git', 'clean', '-fd'])
        gitClean.communicate()

        gitCheckOutMain = subprocess.Popen(['git', 'checkout', 'main'])
        gitCheckOutMain.communicate()

        gitDeleteBranch = subprocess.Popen(['git', 'branch', '-D', branch])
        gitDeleteBranch.communicate()

        if book != '':

            os.chdir(eswatiniRepositoryBooks)

            shutil.rmtree(book)

        os.chdir(jupyterDirectory)

        configOb.set('USERINFO', 'branch', '')
        configOb.set('USERINFO', 'book', '')

        with open('config.ini', 'w') as conf:
            configOb.write(conf)

def launchJupyterLabs():

    path = jupyter.replace("\\", "/")
    command = 'cmd /k "py -m jupyterlab --notebook-dir=' + path + '"'

    os.chdir(owd)
    subprocess.Popen(command, creationflags = subprocess.CREATE_NEW_CONSOLE) #Opens jupyter lab in a new terminal

###########################################################################################################
#Creating File Folder Path Names
###########################################################################################################

parent_dir = os.path.expanduser('~')

#original working directory
owd = os.getcwd()

#Local Repository Paths
jupyterDirectory = ''
jupyter = ''
jupyterBooks = ''
jupyterNotebooks = ''
notebookHTMLS = ''
zippedJupyterBooks = ''
jupyterImages = ''

#Eswatini Repository Paths
eswatiniRepository = ''
eswatiniRepositoryNotebooks = ''
eswatiniRepositoryHTML = ''
eswatiniRepositoryBooks = ''
eswatiniRepositoryZippedBooks = ''
eswatiniRepositoryImages = ''

createPaths()

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
# print('eswatiniRepositoryImages: ', eswatiniRepositoryImages, sep=None)
# print("---------------------------------")

# ###########################################################################################################
# #Installing Dependencies
# ###########################################################################################################

# required  = {'jupyterlab', 'jupyter-book', 'nbconvert[webpdf]'} 
# installed = {pkg.key for pkg in pkg_resources.working_set}
# missing   = required - installed

# if missing:

#     #implementing pip as a subprocess:
#     subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# #Githubs CLI must be installed with Scoop
# #Installing Scoop
# subprocess.run(["powershell", "Set-ExecutionPolicy RemoteSigned -scope CurrentUser"]) #sets permissions on PowerShell so that scoop can be installed

# updateScoop = os.path.expanduser('~')
# updateScoop = updateScoop + "\scoop\shims\scoop update scoop"

# try: #Try to update Scoop
#     subprocess.run(["powershell", "-Command", updateScoop], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# except subprocess.CalledProcessError: #If we can't update scoop it must not be installed so install scoop

#     subprocess.run(["powershell", "-Command", "iwr -useb get.scoop.sh | iex"])

# #Installing GitHubs CLI
# installGH = os.path.expanduser('~')
# installGH = installGH + "\scoop\shims\scoop install gh"

# updateGH = os.path.expanduser('~')
# updateGH = updateGH + "\scoop\shims\scoop update gh"

# ghPath = os.path.expanduser('~')
# ghPath = ghPath + "\scoop\shims\gh.exe"

# if os.path.isfile(ghPath) == False:

#     subprocess.run(["powershell", "-Command", installGH])

#     print('Your computer now needs to restart in order to ensure Scoop and GH are on PATH')
#     print('Once this program has closed, please restart your computer before running this program again')
#     print('Running this program before restarting your computer may result in errors in the program.')
#     tempRestart = input("Press enter to exit") #RESTARTING BUT NOT TAKING IO AFTER RESTARTING
#     exit()

###########################################################################################################
#First Time Setup
###########################################################################################################

if (os.path.exists(jupyterDirectory)) is False:

    print("Performing first time setup\n")
    print("A file system for storing your Jupyter Books and Notebooks, as well as the Eswatini Repository")
    print("will be created in your documents folder\n")
    print("Creating File Folder system...\n")

    ###########################################################################################################
    #Installing Dependencies
    ###########################################################################################################

    required  = {'jupyterlab', 'jupyter-book', 'nbconvert[webpdf]'} 
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing   = required - installed

    if missing:

        #implementing pip as a subprocess:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    #Githubs CLI must be installed with Scoop
    #Installing Scoop
    subprocess.run(["powershell", "Set-ExecutionPolicy RemoteSigned -scope CurrentUser"]) #sets permissions on PowerShell so that scoop can be installed

    updateScoop = os.path.expanduser('~')
    updateScoop = updateScoop + "\scoop\shims\scoop update scoop"

    try: #Try to update Scoop
        subprocess.run(["powershell", "-Command", updateScoop], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    except subprocess.CalledProcessError: #If we can't update scoop it must not be installed so install scoop

        subprocess.run(["powershell", "-Command", "iwr -useb get.scoop.sh | iex"])

    #Installing GitHubs CLI
    installGH = os.path.expanduser('~')
    installGH = installGH + "\scoop\shims\scoop install gh"

    updateGH = os.path.expanduser('~')
    updateGH = updateGH + "\scoop\shims\scoop update gh"

    ghPath = os.path.expanduser('~')
    ghPath = ghPath + "\scoop\shims\gh.exe"

    if os.path.isfile(ghPath) == False:

        subprocess.run(["powershell", "-Command", installGH])

        print('Your computer now needs to restart in order to ensure Scoop and GH are on PATH')
        print('Once this program has closed, please restart your computer before running this program again')
        print('Running this program before restarting your computer may result in errors in the program.')
        tempRestart = input("Press enter to exit") #RESTARTING BUT NOT TAKING IO AFTER RESTARTING
        exit()

    ###########################################################################################################
    #Creating File Folder System
    ###########################################################################################################

    createFileFolders()

    ###########################################################################################################
    #Creating Config File
    ###########################################################################################################

    createConfigFile()

    ###########################################################################################################
    #Logging User into Github using CLI
    ###########################################################################################################
    
    logIntoGitHub()

    ###########################################################################################################
    #Cloning Eswatini Repository
    ###########################################################################################################

    cloneRepository()

    ###########################################################################################################
    #Setting Git Config user and email settings
    ###########################################################################################################
    
    setGitConfig()

###########################################################################################################
#First Time Setup Already Done
###########################################################################################################

else:

    print("First time set up already done.\n")

    ###########################################################################################################
    #Logging User into Github
    ###########################################################################################################
    
    logIntoGitHub()

    ###########################################################################################################
    #Updating Repository
    ###########################################################################################################

    updateRepository()

    ###########################################################################################################
    #Deleteing existing branch
    ###########################################################################################################

    deleteBranch()

###########################################################################################################
#PROGRAM MAIN MENU LOOP
###########################################################################################################

#Main Menu Loop

mainLoopConditional = True #True for staying in the loop, False for exiting the loop

print("\n-------------------------------------------------------------------------------\n")

while mainLoopConditional == True:

    mainMenuAnswer = True #True for staying in the loop, False for exiting the loop

    while mainMenuAnswer == True:

        mainMenu = [
            "Main Menu",
            "Open Jupyter Lab where you can create or edit Jupyter Notebooks",
            "Create a new Jupyter Book",
            "Upload a Jupyter Notebook or Book to the Eswatini textbook resource website",
            "Options Menu",
            "Help",
            "Exit",
        ]

        mainMenuCaptions = [0]
        mainMenuChoice = mainMenu[cutie.select(mainMenu, caption_indices = mainMenuCaptions, selected_index = 1)]

        #Open Jupyter Lab where you can create or edit Jupyter Notebooks
        if mainMenuChoice == "Open Jupyter Lab where you can create or edit Jupyter Notebooks":
            mainMenuOption = 1
            mainMenuAnswer = False

        #Create a new Jupyter Book
        elif  mainMenuChoice ==  "Create a new Jupyter Book":
            mainMenuOption = 2
            mainMenuAnswer = False

        #Upload a Jupyter Notebook or Book to the Eswatini textbook resource website
        elif mainMenuChoice == "Upload a Jupyter Notebook or Book to the Eswatini textbook resource website":
            mainMenuOption = 3
            mainMenuAnswer = False

        #Options Menu
        elif mainMenuChoice == "Options Menu":
            mainMenuOption = 4
            mainMenuAnswer = False

        #Help
        elif mainMenuChoice == "Help":
            mainMenuOption = 5
            mainMenuAnswer = False
            
        #Exit
        elif mainMenuChoice == "Exit":
            mainMenuOption = 6
            mainMenuAnswer = False

        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

    ###########################################################################################################
    #1)Open Jupyter Lab where you can create or edit Jupyter Notebooks
    ###########################################################################################################

    if mainMenuOption == 1:

        print("\n-------------------------------------------------------------------------------\n")
        print("Opening Jupyter Labs.")
        print("This will open in a new terminal.")
        print("This terminal will pause until you have closed the Jupyter Notebook Terminal.")
        print()

        launchJupyterLabs()

        print()
        print('Exit Menu')

        #Exit choice one menu

        jupyterLabsExitMenuAnswer = True #True for staying in the loop, False for exiting the loop

        while jupyterLabsExitMenuAnswer == True:

            jupyterLabsMenu = [
                "Return to Main Menu",
                "Exit",
            ]

            jupyterLabsExitMenuChoice = jupyterLabsMenu[cutie.select(jupyterLabsMenu, selected_index = 0)]

            #Return to Main Menu
            if jupyterLabsExitMenuChoice == "Return to Main Menu":

                print("\n-------------------------------------------------------------------------------\n")
                jupyterLabsExitMenuAnswer = False

            #Exit
            elif jupyterLabsExitMenuChoice == "Exit":

                print()
                jupyterLabsExitMenuAnswer = False
                mainLoopConditional == False
                exit()

            else:
                print("Invalid choice. Please enter a number between 1 and 2.")
       
    ###########################################################################################################
    #2)Create a new Jupyter Book
    ###########################################################################################################

    elif mainMenuOption == 2:
        
        os.chdir(jupyterBooks)

        createJupyterBook = True #True for staying in the loop, False for exiting the loop

        while createJupyterBook is True: 

            print("\n-------------------------------------------------------------------------------")

            bookName = input("\nWhat is the name of your new Jupyter Book(Note that spaces will be removed): ")
            bookName = bookName.replace(" ","")
            bookName = bookName.replace("'", "")

            if os.path.exists(os.path.join(jupyterBooks, bookName)) is False: #If user doesn't already have a book by that name in their own repository

                createJupyterBook = False

                #Creating a new jupyter book with the given name
                jbCommand = "jupyter-book create " + bookName
                os.chdir(jupyterBooks)
                subprocess.call(jbCommand)
                print("-------------------------------------------------------------------------------\n")
            
            else:

                print("\nThat book already exists, please either delete it or choose a different name\n")

                jupyterBookMenu = [
                    "Return to Main Menu",
                    "Choose a New Name",
                ]

                jupyterBookMenuChoice = jupyterBookMenu[cutie.select(jupyterBookMenu, selected_index = 0)]

                if jupyterBookMenuChoice == "Return to Main Menu":

                    print("\n-------------------------------------------------------------------------------\n")
                    createJupyterBook = False

                #Exit
                elif jupyterBookMenuChoice == "Choose a New Name":

                    continue

                else:
                    print("Invalid choice")
                

        os.chdir(owd)

    ###########################################################################################################
    #3)Upload a Jupyter Notebook or Book to the Eswatini textbook resource website
    ###########################################################################################################

    #Choosing either a Jupyter Book or Notebook Loop

    elif mainMenuOption == 3:

        bookOrNotebookMenuAnswer = True #True for staying in the loop, False for exiting the loop

        while bookOrNotebookMenuAnswer == True:

            print("\n-------------------------------------------------------------------------------\n")

            bookOrNoteBookMenu = [
                "What would you like to upload?",
                "Jupyter Notebook",
                "Jupyter Book",
                "Return to Main Menu",
            ]

            bookOrNotebookCaptions = [0]
            bookOrNotebookChoice = bookOrNoteBookMenu[cutie.select(bookOrNoteBookMenu, caption_indices = bookOrNotebookCaptions, selected_index = 1)]

            #Jupyter Notebook
            if bookOrNotebookChoice == "Jupyter Notebook":
                
                bookOrNotebookMenuOption = 1
                bookOrNotebookMenuAnswer = False
                print()

            #Jupyter Book
            elif bookOrNotebookChoice == "Jupyter Book":
                
                bookOrNotebookMenuOption = 2
                bookOrNotebookMenuAnswer = False
                print()

            #Return to Main Menu
            elif bookOrNotebookChoice == "Return to Main Menu":

                bookOrNotebookMenuOption = 3
                bookOrNotebookMenuAnswer = False
                print("\n-------------------------------------------------------------------------------\n")

            else:

                print("Invalid choice.")

        #Uploading a Jupyter Notebook

        if bookOrNotebookMenuOption == 1:

            #Creating new branch to apply changes to
            updateRepository()

            os.chdir(jupyterDirectory)

            time = datetime.now().strftime('%H:%M:%S')

            configOb = ConfigParser()
            configOb.read('config.ini')
            userInfo = configOb['USERINFO']
            tempBranchUsername = userInfo['username']

            branchName = tempBranchUsername + "_PullRequest_" + time
            branchName = branchName.replace(" ","")
            branchName = branchName.replace("'", "")
            branchName = branchName.replace(":", "")

            configOb.set('USERINFO', 'branch', branchName)

            with open('config.ini', 'w') as conf:
                configOb.write(conf)

            os.chdir(eswatiniRepository)

            gitMakeNewBranch = subprocess.Popen(['git', 'branch', branchName])
            gitMakeNewBranch.communicate()

            #Checking out new branch for pull request
            gitCheckOutNewBranch = subprocess.Popen(['git', 'checkout', branchName])
            gitCheckOutNewBranch.communicate()

            print()

            os.chdir(jupyterNotebooks)

            existingNotebooks = [] #Will hold all the notebooks stored in the users directory

            #Variables to be written into the textbooks.json file
            notebookAuthor = ""
            notebookClass = ""
            notebookDescription = ""
            notebookHTML = ""
            notebookFile = ""
            notebookImage = ""
            notebookName = ""
            notebookSubject = ""
            
            #Getting Books from user directory for Jupyter Notebooks
            for x in os.listdir(): #Getting notebooks that exist in the users Notebook repository
                if x.endswith(".ipynb"):
                    existingNotebooks.append(x)

            whichNotebookAnswer = True #True for staying in the loop, False for exiting the loop

            skipIsFileCheck = 0 #Causes program to skip checking if the picked file exists in the Eswatini Repository (0: check, 1: skip)

            if not existingNotebooks: #No notebooks in the users repository

                print('You have no Jupyter Notebooks in this directory.')
                print('Returning to Main Menu\n')
                deleteBranch()
                print("\n-------------------------------------------------------------------------------\n")
                
                skipIsFileCheck = 1 #Causes the program to skip the isFile check next.
                whichNotebookAnswer = False #True for staying in the loop, False for exiting the loop
            
            else:

                existingNotebooks.insert(0, "Which Jupyter Notebook would you like to upload?")

            #Getting the user to select which notebook they want to upload
            while whichNotebookAnswer == True:

                print("-------------------------------------------------------------------------------\n")

                existingNotebooksCaptions = [0]
                notebookToBeUploaded = existingNotebooks[cutie.select(existingNotebooks, caption_indices = existingNotebooksCaptions, selected_index = 1)]

                print()

                if cutie.prompt_yes_or_no("You have selected " + notebookToBeUploaded + ". Is this correct?"):

                    print()
                    whichNotebookAnswer = False
                
                else:

                    print()

                    if cutie.prompt_yes_or_no("Would you like to select a different Notebook?"):
                        
                        print()
                        continue

                    else:

                        whichNotebookAnswer = False
                        skipIsFileCheck = 1
                        print("\nReturning to Main Menu\n")
                        deleteBranch()
                        print("\n-------------------------------------------------------------------------------\n")

            
            os.chdir(eswatiniRepositoryNotebooks)

            #Seeing if the choosen notebook is already in the repository
            if skipIsFileCheck == 0:

                #Checking if that notebook name already exists
                if os.path.isfile(notebookToBeUploaded) == True: #Stops user from uploading a Notebook thats name already exists
                                                                 #Prevents pathing issues on the website
                    print()
                    print("A Jupyter Notebook by that name already exists.")
                    print("Please contact the website moderator to remove the Notebook, or choose a different name for the book.")
                    print("Returning to the Main Menu\n")
                    deleteBranch()
                    print("\n-------------------------------------------------------------------------------\n")
                    exitNotebook = 0 #Causes the program to skip back to the main menu

                else:
                    
                    #Copying 'notebook to be uploaded' into the HTML folder and creating an HTML version then removing 'notebook to be uploaded' from the HTML folder

                    os.chdir(jupyterNotebooks)
                    shutil.copy(notebookToBeUploaded, eswatiniRepositoryNotebooks)
                    shutil.copy(notebookToBeUploaded, notebookHTMLS)

                    os.chdir(notebookHTMLS)
                    convertNotebookToHTML = subprocess.Popen(['jupyter', 'nbconvert', '--to', 'HTML', notebookToBeUploaded], stdout=DEVNULL, stderr=STDOUT)
                    convertNotebookToHTML.communicate()

                    #getting html filename (with .html file ending) and moving it to correct folder
                    htmlFile = os.path.splitext(notebookToBeUploaded)[0] + '.html' 
                    shutil.copy(htmlFile, eswatiniRepositoryHTML)

                    os.remove(notebookToBeUploaded)
                    os.chdir(owd)

                    #Creating the path the website will use
                    notebookFile = "books/juypterNotebooks/" + notebookToBeUploaded
                    notebookHTML = "books/jupyterNotebookHTML/" + htmlFile
                    exitNotebook = 1
                
            else:

                exitNotebook = 0

            #Getting from the user which image they wish to upload, if any
            if exitNotebook == 1:

                uploadImageForNotebook = True #True for staying in the loop, False otherwise

                while uploadImageForNotebook == True:
                    
                    print("-------------------------------------------------------------------------------\n")

                    if cutie.prompt_yes_or_no("Is there an image you would like to upload with this Notebook?"):

                        print()
                        uploadImageForNotebookOption = 1
                        uploadImageForNotebook = False
                    
                    else:

                        uploadImageForNotebookOption = 2
                        uploadImageForNotebook = False

                os.chdir(jupyterImages)

                existingNotebookImages = []

                for x in os.listdir(): #Getting images from users image directory
                    existingNotebookImages.append(x)

                #No images in the users repository but user wants one.
                if not existingNotebookImages and uploadImageForNotebookOption == 1: 
                        
                    noNotebookImages = True

                    while noNotebookImages == True:
                        
                        print()
                        print('There are no images currently in your Image directory, would you like to continue without an image?')
                        if cutie.prompt_yes_or_no("Selecting NO will return you to the Main Menu"):

                            noNotebookImages = False
                            uploadImageForNotebookOption = 2

                        else:

                            uploadImageForNotebookOption = 3
                            exitNotebook = 0
                            noNotebookImages = False
                            print("\nReturning to Main Menu\n")
                            deleteBranch()
                            print("\n-------------------------------------------------------------------------------\n")


                if uploadImageForNotebookOption == 1:

                    whichImageToUploadNotebook = True

                    existingNotebookImages.insert(0, 'Which image would you like to upload?')

                    while whichImageToUploadNotebook == True:

                        existingNotebookImagesCaptions = [0]
                        nImage = existingNotebookImages[cutie.select(existingNotebookImages, caption_indices = existingNotebookImagesCaptions, selected_index = 1)]

                        print()

                        if cutie.prompt_yes_or_no("You have selected " + nImage + ". Is this correct?"):

                            os.chdir(eswatiniRepositoryImages)

                            if os.path.isfile(nImage) == True:

                                print()
                                print("An image by that name already exists.")
                                print("Please rename your image before attempting to upload this Notebook again.")
                                print("Returning to the Main Menu\n")
                                deleteBranch()
                                print("\n-------------------------------------------------------------------------------\n")

                                whichImageToUploadNotebook = False #Causes the program to skip back to the main menu
                                uploadImageForNotebookOption = 3
                                exitNotebook = 0 

                            else:

                                os.chdir(jupyterImages)
                                whichImageToUploadNotebook = False
                                shutil.copy(nImage, eswatiniRepositoryImages)
                                notebookImage = 'Img/' + nImage
                        
                        else:

                            print()

                            if cutie.prompt_yes_or_no("Would you like to select a different Image?"):

                                print()
                                continue

                            else:

                                print()

                                if cutie.prompt_yes_or_no("Would you like to continue without an Image?"):

                                    uploadImageForNotebookOption = 2
                                    whichImageToUploadNotebook = False
                                
                                else:

                                    uploadImageForNotebookOption = 3 #Causes the program to skip back to the main menu
                                    exitNotebook = 0
                                    whichImageToUploadNotebook = False
                                    print("\nReturning to Main Menu\n")
                                    deleteBranch()
                                    print("\n-------------------------------------------------------------------------------\n")

                if uploadImageForNotebookOption == 2:

                    notebookImage = ""  

            if exitNotebook == 1: #Book did not already exist and the user wishes to upload it

                os.chdir(eswatiniRepository)

                #Appending the top level keys from textbooks.json into an array (ie: the subjects available to be uploaded to)
                with open('textbooks.json', 'r') as openFile:

                    jsonFile = json.load(openFile)
                    openFile.close()
                
                subjects = []
                
                for i in jsonFile: #Getting subjects from json file

                    subjects.append(i)

                print("\n-------------------------------------------------------------------------------\n")

                #Picking which subject the Notebook belongs to
                whichNotebookSubjectAnswer = True #True for staying in the loop, False for exiting the loop

                subjects.insert(0, 'Which subject does this Jupyter Notebook belong in?')

                while whichNotebookSubjectAnswer == True:

                    subjectsCaptions = [0]
                    notebookSubject = subjects[cutie.select(subjects, caption_indices = subjectsCaptions, selected_index = 1)]

                    print()

                    if cutie.prompt_yes_or_no("You have selected " + notebookSubject + ". Is this correct?"):

                        whichNotebookSubjectAnswer = False
                        print("\n-------------------------------------------------------------------------------")
                    
                    else:
                        
                        print()
                        continue

                os.chdir(eswatiniRepository)

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
                
                #Testing to make sure input is saved correctly
                # print("-------------------------------------------------------------------------------")
                # print('File:', notebookFile, sep=None)
                # print('HTML:', notebookHTML, sep=None)
                # print('Name:', notebookName, sep=None)
                # print('Description:', notebookDescription, sep=None)
                # print('Author:', notebookAuthor, sep=None)
                # print('Class:', notebookClass, sep=None)
                # print('Image:', notebookImage, sep=None)
                # print("-------------------------------------------------------------------------------\n")

                #Writing notebook data to json file
                jsonData = {
                    "file": notebookFile,
                    "zip": "", #Should always be "" for notebooks
                    "html": notebookHTML,
                    "type": "notebook", #Should always be "notebook" for notebooks
                    "name": notebookName,
                    "descript": notebookDescription,
                    "author": notebookAuthor,
                    "class": notebookClass,
                    "image": notebookImage
                }

                jsonFile[notebookSubject].append(jsonData)
                jsonOutFile = open("textbooks.json", "w")
                json.dump(jsonFile, jsonOutFile, indent=3)
                jsonOutFile.close()

                os.chdir(jupyterDirectory)

                #Getting users GitHub username to add to pull request title
                configObj = ConfigParser()
                configObj.read('config.ini')
                userInfo = configOb['USERINFO']
                tempUsername = userInfo['username']

                os.chdir(eswatiniRepository)

                #Git adding all changes to be commited
                gitAdd = subprocess.Popen(['git', 'add', '.'])
                gitAdd.communicate()

                #Commiting local changes
                gitCommit = subprocess.Popen(['git', 'commit', '-m"Pull request for new Jupyter Notebook for ' + tempUsername + '"'])
                gitCommit.communicate()

                print()
                print("------------------------------------------------------------------------------------------------------------")
                print("The program will now create a pull request to the Eswatini Repository")
                print("     1. Please select the first option 'University-of-Eswatini/Eswatini-Project'")
                print("     2. The program will then generate a title for your pull request with your username. Please press enter.")
                print("     3. If you then wish to add comments you can do so by pressing 'e'. Press enter to skip.")
                print("     4. Finally select the first option 'Submit' to submit your pull request.")
                print("------------------------------------------------------------------------------------------------------------")
                print()

                #Creating pull request for commited changes
                ghPullRequest = subprocess.Popen(['gh', 'pr', 'create'])
                ghPullRequest.communicate()

                #Checking out the main branch
                gitCheckOutMain = subprocess.Popen(['git', 'checkout', 'main'])
                gitCheckOutMain.communicate()

                if ghPullRequest.returncode == 0: #Exit Code 0 on PR means successful PR completion

                    #merging PR branch into main after PR
                    gitMerge = subprocess.Popen(['git', 'merge', branchName])
                    gitMerge.communicate()

                    os.chdir(jupyterDirectory)

                    configOb = ConfigParser()
                    configOb.read('config.ini')
                    configOb.set('USERINFO', 'branch', '')

                    with open('config.ini', 'w') as conf:
                        configOb.write(conf)
                    
                    os.chdir(eswatiniRepository)

                    #Deleting pull request branch to keep local repository up to date and prventing branch bloat
                    gitDeleteBranch = subprocess.Popen(['git', 'branch', '-D', branchName])
                    gitDeleteBranch.communicate()

                else:

                    deleteBranch()

                updateRepository()

                print()

        #Uploading a Jupyter Book

        elif bookOrNotebookMenuOption == 2:

            updateRepository()

            os.chdir(jupyterDirectory)

            time = datetime.now().strftime('%H:%M:%S')

            configOb = ConfigParser()
            configOb.read('config.ini')
            userInfo = configOb['USERINFO']
            tempBranchUsername = userInfo['username']

            branchName = tempBranchUsername + "_PullRequest_" + time
            branchName = branchName.replace(" ","")
            branchName = branchName.replace("'", "")
            branchName = branchName.replace(":", "")

            configOb.set('USERINFO', 'branch', branchName)

            with open('config.ini', 'w') as conf:
                configOb.write(conf)

            os.chdir(eswatiniRepository)

            gitMakeNewBranch = subprocess.Popen(['git', 'branch', branchName])
            gitMakeNewBranch.communicate()

            #Checking out new branch for pull request
            gitCheckOutNewBranch = subprocess.Popen(['git', 'checkout', branchName])
            gitCheckOutNewBranch.communicate()

            print()

            os.chdir(jupyterBooks)

            existingBooks = [] #Will hold all the notebooks stored in the users directory

            #Variables to be written into the textbooks.json file
            bookAuthor = ""
            bookClass = ""
            bookDescription = ""
            bookFile = ""
            bookImage = ""
            bookName = ""
            bookSubject = ""
            bookZip = ''

            #Picking which notebook to upload

            for x in os.listdir(): #Getting notebooks that exist in the users Notebook repository
                if x == "ZippedBooks":
                    continue
                else:
                    existingBooks.append(x)

            whichBookAnswer = True #True for staying in the loop, False for exiting the loop

            skipIsFileCheck = 0 #Causes program to skip checking if the picked file exists in the Eswatini Repository (0: check, 1: skip)

            if not existingBooks: #No books in the users repository

                print('You have no Jupyter Books in this directory.')
                print('Returning to Main Menu\n')
                deleteBranch()
                print("\n-------------------------------------------------------------------------------\n")
                skipIsFileCheck = 1 #Causes the program to skip the isFile check next.
                whichBookAnswer = False #True for staying in the loop, False for exiting the loop
            
            else:

                existingBooks.insert(0, 'Which Jupyter Book would you like to upload?')

            #Getting the user to select which book they want to upload
            while whichBookAnswer == True:

                print("-------------------------------------------------------------------------------\n")
                
                existingBooksCaptions = [0]
                bookToBeUploaded = existingBooks[cutie.select(existingBooks, caption_indices = existingBooksCaptions, selected_index = 1)]

                print()

                if cutie.prompt_yes_or_no("You have selected " + bookToBeUploaded + ". Is this correct?"):

                    print()
                    whichBookAnswer = False
                
                else:

                    print()

                    if cutie.prompt_yes_or_no("Would you like to select a different Book?"):

                        print()
                        continue

                    else:

                        whichBookAnswer = False
                        skipIsFileCheck = 1
                        print("\nReturning to Main Menu\n")
                        deleteBranch()
                        print("\n-------------------------------------------------------------------------------\n")

            os.chdir(eswatiniRepositoryBooks)

            #Checking if that book name already exists
            if skipIsFileCheck == 0:

                if os.path.isdir(bookToBeUploaded) == True: #Stops user from uploading a Book thats name already exists
                                                            #Prevents pathing issues on the website
                    print()
                    print("A Jupyter Book by that name already exists.")
                    print("Please contact the website moderator to remove the book, or choose a different name for the book.")
                    print("Returning to the Main Menu\n")
                    deleteBranch()
                    print("\n-------------------------------------------------------------------------------\n")
                    exitBook = 0
                
                else:

                    print("Building Jupyer Book...\n")

                    #Adding the book name to the config file
                    os.chdir(jupyterDirectory)
                    configOb = ConfigParser()
                    configOb.read('config.ini')
                    configOb.set('USERINFO', 'book', bookToBeUploaded)

                    with open('config.ini', 'w') as conf:
                        configOb.write(conf)                   
                    print("ADDED TO CONFIG")

                    os.chdir(jupyterBooks)

                    #Building HTML version of the Book to be uploaded
                    buildBook = subprocess.Popen(['jupyter-book', 'build', bookToBeUploaded], stdout=DEVNULL, stderr=STDOUT)
                    buildBook.communicate()
                    print("HTML BOOK BUILT")

                    #Copying book into the correct folder in eswatini repository
                    tempBookPath = os.path.join(eswatiniRepositoryBooks, bookToBeUploaded)
                    shutil.copytree(bookToBeUploaded, tempBookPath)
                    print("BOOK COPIED")

                    #Zipping the Book to be 
                    make_archive(bookToBeUploaded, "zip")
                    print("BOOK ZIPPED")

                    # #Copying book to the zipped books folder to be zipped
                    # tempBookPath = os.path.join(zippedJupyterBooks, bookToBeUploaded)
                    # shutil.copytree(bookToBeUploaded, tempBookPath)
                    # print("BOOK COPIED FOR ZIP")

                    # #Zipping the Book to be uploaded and removing the unzipped version
                    # os.chdir(zippedJupyterBooks)
                    # make_archive(bookToBeUploaded, "zip")
                    # shutil.rmtree(bookToBeUploaded)
                    
                    #Copying Zipped Book to be uploaded to the correct folder in eswatini repository
                    zippedBook = bookToBeUploaded + ".zip"
                    tempBookPath = os.path.join(eswatiniRepositoryZippedBooks, zippedBook)
                    print("Attempting to copy zipped file")
                    shutil.copy(zippedBook, eswatiniRepositoryZippedBooks)
                    print("ZIP COPIED")

                    #Deleting zipped file
                    os.remove(zippedBook)

                    #Creating the path(s) for zipped and unzipped books that the website will use
                    bookFile = "books/juypterBooks/" + bookToBeUploaded + "/_build/html/index.html"
                    zippedBookFile = "books/zippedJuypterBooks/" + bookToBeUploaded + ".zip"
                    print("BOOK AND ZIP FILES MADE")

                    os.chdir(jupyterBooks)

                    exitBook = 1

            else:

                exitBook = 0

            #Getting from the user which image the wish to upload, if any
            if exitBook == 1:
                
                uploadImageForBook = True #True for staying in the loop, False otherwise

                while uploadImageForBook == True:
                    
                    # print()
                    # print("Is there an image you would like to upload with this Book?")
                    # print("1) Yes")
                    # print("2) No")

                    # try:
                    #     uploadImageForBookOption = int(input('Enter your choice: '))
                    
                    # except:
                    #     print('Wrong input. Please enter either 1 or 2')
                    
                    # if uploadImageForBookOption == 1 or uploadImageForBookOption == 2:

                    #     uploadImageForBook = False

                    # else:

                    #     print("Invalid choice. Please enter either 1 or 2")

                    print("-------------------------------------------------------------------------------\n")

                    if cutie.prompt_yes_or_no("Is there an image you would like to upload with this Book?"):

                        print()
                        uploadImageForBookOption = 1
                        uploadImageForBook = False
                    
                    else:

                        uploadImageForBookOption = 2
                        uploadImageForBook = False
                
                os.chdir(jupyterImages)

                existingBookImages = []

                #No images in the users repository but user wants one
                for x in os.listdir(): #Getting images from users image directory
                    existingBookImages.append(x)
                
                if not existingBookImages and uploadImageForBookOption == 1:

                    noBookImages = True

                    while noBookImages == True:

                        # print()
                        # print('There are no images currently in your Image directory, would you like to continue without an image?')
                        # print('Selecting NO will return you to the main menu')
                        # print()
                        # print("1) Yes")
                        # print("2) No")

                        # try:
                        #     noBookImagesOption = int(input('Enter your choice: '))
                        # except:
                        #     print('Invalid choice. Please enter either 1 or 2.')
                            
                        # if noBookImagesOption == 1:

                        #     noBookImages = False
                        #     uploadImageForBookOption = 2

                        # elif noBookImagesOption == 2:

                        #     uploadImageForBookOption = 3
                        #     exitBook = 0
                        #     noBookImages = False
                        #     deleteBranch()

                        # else:

                        #     print("Invalid choice. Please enter either 1 or 2.\n")

                        print()
                        print("There are no images currently in your Image directory, would you like to continue without an image?")
                        if cutie.prompt_yes_or_no("Selecting NO will return you to the Main Menu"):

                            noBookImages = False
                            uploadImageForBookOption = 2

                        else:

                            uploadImageForBookOption = 3
                            exitBook = 0
                            noBookImages = False
                            print("\nReturning to Main Menu\n")
                            deleteBranch()
                            print("\n-------------------------------------------------------------------------------\n")                    

                if uploadImageForBookOption == 1:

                    whichImageToUploadBook = True

                    existingBookImages.insert(0, 'Which image would you like to upload?')

                    while whichImageToUploadBook == True:

                        existingBookImagesCaptions = [0]
                        bImage = existingBookImages[cutie.select(existingBookImages, caption_indices = existingBookImagesCaptions, selected_index = 1)]

                        print()

                        if cutie.prompt_yes_or_no("You have selected " + bImage + ". Is this correct?"):

                            os.chdir(eswatiniRepositoryImages)

                            if os.path.isfile(bImage):

                                print()
                                print("An image by that name already exists.")
                                print("Please rename your image before attempting to upload this Notebook again.")
                                print("Returning to the Main Menu\n")
                                deleteBranch()
                                print("\n-------------------------------------------------------------------------------\n")

                                whichImageToUploadBook = False
                                uploadImageForBookOption = 3
                                exitBook = 0

                            else:

                                os.chdir(jupyterImages)
                                whichImageToUploadBook = False
                                shutil.copy(bImage, eswatiniRepositoryImages)
                                bookImage = 'Img/' + bImage
                        
                        else:

                            print()

                            if cutie.prompt_yes_or_no("Would you like to select a different Image?"):

                                print()
                                continue

                            else:

                                print()

                                if cutie.prompt_yes_or_no("Would you like to continue without an Image?"):

                                    uploadImageForBookOption = 2
                                    whichImageToUploadBook = False
                                
                                else:

                                    uploadImageForBookOption = 3
                                    exitBook = 0
                                    whichImageToUploadBook = False
                                    print("\nReturning to Main Menu\n")
                                    deleteBranch()
                                    print("\n-------------------------------------------------------------------------------\n")
                
                if uploadImageForBookOption == 2:

                    bookImage = ""

            if exitBook == 1: #Book did not already exist and the user wishes to upload it

                os.chdir(eswatiniRepository)

                #Appending the top level keys from textbooks.json into an array (ie: the subjects available to be uploaded to)
                with open('textbooks.json', 'r') as openFile:

                    jsonFile = json.load(openFile)
                    openFile.close()
                    
                subjects = []
                    
                for i in jsonFile: #Getting subjects from json file

                    subjects.append(i)

                print("\n-------------------------------------------------------------------------------\n")

                #Picking which subject the Book belongs to
                whichBookSubjectAnswer = True #True for staying in the loop, False for exiting the loop

                subjects.insert(0, 'Which subject does this Jupyter Book belong in?')

                while whichBookSubjectAnswer == True:

                    # for i in range(len(subjects)):

                    #     print(i+1, ')', subjects[i], sep=None)
                        
                    # print()

                    # try:
                    #     whichBookSubjectOption = int(input('Enter your choice: '))
                    # except:
                    #     print('Wrong input. Please enter a number between 1 and ', len(subjects), '.', sep=None)
                        
                    # if whichBookSubjectOption > 0 and whichBookSubjectOption <= len(subjects):

                    #     whichBookSubjectAnswer = False
                    #     bookSubject = subjects[whichBookSubjectOption-1]
                        
                    # else:

                    #     print("Invalid choice. Please enter a number between 1 and ", len(subjects), sep=None)
                    #     print()
                    #     print('Which subject does this Jupyter Book belong in?\n')

                    subjectsCaptions = [0]
                    bookSubject = subjects[cutie.select(subjects, caption_indices = subjectsCaptions, selected_index = 1)]

                    print()

                    if cutie.prompt_yes_or_no("You have selected " + bookSubject + ". Is this correct?"):

                        whichBookSubjectAnswer = False
                        print("\n-------------------------------------------------------------------------------")
                    
                    else:

                        print()
                        continue

                os.chdir(eswatiniRepository)

                #Getting pertinant information from the user and saving to variables that will be written to textbooks.json
                print()
                bookName = input("What is this Books title: ")
                print()
                bookClass = input("What class is this Book for: ")
                print()
                bookAuthor = input("Who is the author of this Book: ")
                print()
                bookDescription = input("Please enter a short description of your Book: ")
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
                    "html" : "", #Should always be "" for Jupyter Books
                    "type": "book", #Should always be "book" for Jupyter Books
                    "name": bookName,
                    "descript": bookDescription,
                    "author": bookAuthor,
                    "class": bookClass,
                    "image": bookImage
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

                #Git adding all changes to be commited
                gitAdd = subprocess.Popen(['git', 'add', '.'])
                gitAdd.communicate()

                #Commiting local changes
                gitCommit = subprocess.Popen(['git', 'commit', '-m"Pull request for new Jupyter Book for ' + tempUsername + '"'])
                gitCommit.communicate()

                print()
                print("------------------------------------------------------------------------------------------------------------")
                print("The program will now create a pull request to the Eswatini Repository")
                print("     1. Please select the first option 'University-of-Eswatini/Eswatini-Project'")
                print("     2. The program will then generate a title for your pull request with your username. Please press enter.")
                print("     3. If you then wish to add comments you can do so by pressing 'e'. Press enter to skip.")
                print("     4. Finally select the first option 'Submit' to submit your pull request.")
                print("------------------------------------------------------------------------------------------------------------")
                print()

                #Creating pull request for commited changes
                ghPullRequest = subprocess.Popen(['gh', 'pr', 'create'])
                ghPullRequest.communicate()

                #Checking out the main branch
                gitCheckOutMain = subprocess.Popen(['git', 'checkout', 'main'])
                gitCheckOutMain.communicate()

                if ghPullRequest.returncode == 0: #Exit Code 0 on PR means successful PR completion

                    #merging PR branch into main after PR
                    gitMerge = subprocess.Popen(['git', 'merge', branchName])
                    gitMerge.communicate()

                    os.chdir(jupyterDirectory)

                    configOb = ConfigParser()
                    configOb.read('config.ini')

                    #Don't need to remember branch name or book name as PR was successfull
                    configOb.set('USERINFO', 'branch', '')
                    configOb.set('USERINFO', 'book', '')

                    with open('config.ini', 'w') as conf:
                        configOb.write(conf)

                    os.chdir(eswatiniRepository)

                    #Deleting pull request branch to keep local repository up to date and prventing branch bloat
                    gitDeleteBranch = subprocess.Popen(['git', 'branch', '-D', branchName])
                    gitDeleteBranch.communicate()
                
                else:

                    deleteBranch()

                updateRepository()

                print()

        #Returning to Main Menu

        elif bookOrNotebookMenuOption == 3:

            continue

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
                print("\n-------------------------------------------------------------------------------\n")
                
                # print("Options Menu")
                # print("1) Update your Eswatini Repository (Git Pull)")
                # print("2) Update your GitHub credentials (Username / Email / Personal Access Token)")
                # print("3) Log out of GitHub")
                # print("4) Log into GitHub")
                # print("5) Exit to Main Menu")

                # optionsMenuOption = ''

                # try:
                #     optionsMenuOption = int(input('Enter your choice: '))
                # except:
                #     print('Invalid choice. Please enter a number between 1 and 5.')

                optionsMenu = [
                    "Options Menu",
                    "Update your Eswatini Repository (Git Pull)",
                    "Update your GitHub credentials (Username / Email / Personal Access Token)",
                    "Log out of GitHub",
                    "Log into GitHub",
                    "Exit to Main Menu",
                ]

                optionsMenuCaptions = [0]
                optionsMenuChoice = optionsMenu[cutie.select(optionsMenu, caption_indices = optionsMenuCaptions, selected_index = 1)]

                #Update your Eswatini Repository (Git Pull)
                if optionsMenuChoice == "Update your Eswatini Repository (Git Pull)":
                        
                    print()
                    optionsMenuOption = 1
                    optionsMenuAnswer = False

                #Update your GitHub credentials (Username / Email / Personal Access Token)
                elif optionsMenuChoice == "Update your GitHub credentials (Username / Email / Personal Access Token)":

                    print()
                    optionsMenuOption = 2
                    optionsMenuAnswer = False

                #Log out of GitHub
                elif optionsMenuChoice == "Log out of GitHub":

                    print()
                    optionsMenuOption = 3
                    optionsMenuAnswer = False

                #Log into GitHub
                elif optionsMenuChoice == "Log into GitHub":

                    print()
                    optionsMenuOption = 4
                    optionsMenuAnswer = False
                
                #Exit to Main Menu
                elif optionsMenuChoice == "Exit to Main Menu":

                    print()
                    optionsMenuOption = 5
                    optionsMenuAnswer = False

                else:
                    print("Invalid choice.")

            #Update your Eswatini Repository (Git Pull)
            if optionsMenuOption == 1:
                
                updateRepository()

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
                print("\n-------------------------------------------------------------------------------\n")
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
        print("    3) It is recomended that you regularly go to 'Options' and update your local repository. It is also recomended you do this before choosing to upload a new Book or Notebook.\n")
        tempEnterToExitHelp = input("Press ENTER to return to the main menu")
    
    ###########################################################################################################
    #5)Exit
    ###########################################################################################################

    elif mainMenuOption == 6:

        print("\n-------------------------------------------------------------------------------\n")
        print("Exiting...\n\n-------------------------------------------------------------------------------\n")
        exit()

    ###########################################################################################################
    #How did you get here?
    ###########################################################################################################

    else:

        print("How did you get here?")