#IMPORTS
from ast import main
from asyncio import subprocess
import os
import io
import sys
import pip
import subprocess
from configparser import ConfigParser

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

print("---------------------------------")
print(owd)
print(jupyterDirectory)
print(jupyter)
print(jupyterBooks)
print(jupyterNotebooks)
print(zippedJupyterBooks)
print(eswatiniRepository)
print("---------------------------------")

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

    print("Installing GitPython...\n")

    pip.main(["install", "--user", "gitpython"])

    print()

    import git
    from git import Repo

    ###########################################################################################################
    #Cloning Eswatini Repository
    ###########################################################################################################

    print("Cloning Eswatini repository...\n")

    git.Repo.clone_from('https://github.com/University-of-Eswatini/Eswatini-Project.git', eswatiniRepository)

    ###########################################################################################################
    #Installing Jupyter Labs and BooksInstalling Jupyter Labs and Books
    ###########################################################################################################

    print("Installing Jupyter Labs...\n")
    pip.main(["install", "--user", "jupyterlab"]) #os.system('cmd /k "py -m jupyterlab"') opens jupyter lab
    print()

    print("Installing Jupyter Books...\n")
    pip.main(["install", "--user", "jupyter-book"]) #os.system('cmd /k "jb --help"') jupyter books
    print()

    ###########################################################################################################
    #Installing GitHubs CLI commands
    ###########################################################################################################

    

else:

    print("First time set up already done\n\n")

mainLoopConditional = True #True for staying in the loop, False for exiting the loop

while mainLoopConditional == True:

    mainMenuAnswer = True #True for staying in the loop, False for exiting the loop

    while mainMenuAnswer == True:

        print("-------------------------------------------------------------------------------")
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
            print("-------------------------------------------------------------------------------")
        except:
            print('Wrong input. Please enter a number.')

        if mainMenuOption == 1:
            mainMenuAnswer = False
            break

        elif mainMenuOption == 2:
            mainMenuAnswer = False
            break

        elif mainMenuOption == 3:
            mainMenuAnswer = False
            break

        elif mainMenuOption == 4:
            mainMenuAnswer = False
            break

        elif mainMenuOption == 5:
            mainMenuAnswer = False
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 5")
    
    #print()
    #print("You chose: " + str(mainMenuOption))

    ###########################################################################################################
    #1)Open Jupyter Lab where you can create or edit Jupyter Notebooks
    ###########################################################################################################

    if mainMenuOption == 1:

        print("Opening Jupyter Labs")
        print("This will open in a new terminal")

        path = jupyter.replace("\\", "/")
        command = 'cmd /k "py -m jupyterlab --notebook-dir=' + path + '"'

        os.chdir(owd)
        subprocess.call(command, creationflags = subprocess.CREATE_NEW_CONSOLE)

        #Exit choice one menu

        choiceOneExitMenuAnswer = True

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
                choiceOneExitMenuAnswer = False
                break

            elif choiceOneExitMenuOption == 2:
                choiceOneExitMenuAnswer = False
                mainLoopConditional == False
                break

            else:
                print("Invalid choice. Please enter a number between 1 and 2")

    ###########################################################################################################
    #2)Create a new Jupyter Book
    ###########################################################################################################

    elif mainMenuOption == 2:

        print("You choose 2")

    ###########################################################################################################
    #3)Upload a Jupyter Notebook or Book to the Eswatini textbook resource website
    ###########################################################################################################

    elif mainMenuOption == 3:

        print("You chose 3")

    ###########################################################################################################
    #4)Options Menu
    ###########################################################################################################

    elif mainMenuOption == 4:

        print("You chose 4")

    ###########################################################################################################
    #5)Exit
    ###########################################################################################################

    elif mainMenuOption == 5:

        print("You chose 5")

    ###########################################################################################################
    #How did you get here?
    ###########################################################################################################

    else:

        print("How did you get here?")