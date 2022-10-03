#IMPORTS
import os
import io
import sys
import pip

from configparser import ConfigParser

###### Creating File Folder System ########################################################################
###########################################################################################################

parent_dir = os.path.expanduser('~')
parent_dir = parent_dir + "\OneDrive\Documents"
owd = os.getcwd() #original working directory
jupyterDirectory = os.path.join(parent_dir, "JupyterDirectory")

if (os.path.exists(jupyterDirectory)) is False:

    print("Performing first time setup\n")
    print("A file system for storing your Jupyter Books and Notebooks, as well as the Eswatini Repository")
    print("will be created in your documents folder\n")
    print("Creating File Folder system...\n")


    ###### Creating File Folder System ########################################################################

    #creating Jupyter Directory
    jupyterDirectory = os.path.join(parent_dir, "JupyterDirectory")
    os.mkdir(jupyterDirectory)

    #Creating folder to hold Jupyter Books and Jupyter Notebooks folders
    jupyter = os.path.join(jupyterDirectory, "Jupyter")
    os.mkdir(jupyter)

    #Creating folder to hold Jupyter Books 
    jupyterBooks = os.path.join(jupyter, "JupyterBooks")
    os.mkdir(jupyterBooks)

    #Creating folder to hold Jupyter Notebooks
    jupyterNotebooks = os.path.join(jupyter, "JupyterNotebooks")
    os.mkdir(jupyterNotebooks)

    #Creating folder to hold zipped Jupyter Books
    zippedJupyterBooks = os.path.join(jupyterBooks, "ZippedJupyterBooks")
    os.mkdir(zippedJupyterBooks)

    #Creating folder to hold Eswatini Repository
    eswatiniRepository = os.path.join(jupyterDirectory, "EswatiniRepository")
    os.mkdir(eswatiniRepository)

    ###### Creating Config File ###############################################################################

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

    ###### Installing GitPython ###############################################################################

    print("Installing GitPython...\n")

    pip.main(["install", "--user", "gitpython"])

    print()

    import git
    from git import Repo

    ###### Cloning Eswatini Repository ########################################################################

    print("Cloning Eswatini repository...\n")

    git.Repo.clone_from('https://github.com/University-of-Eswatini/Eswatini-Project.git', eswatiniRepository)

    ###### Installing Jupyter Labs and Books###################################################################

    print("Installing Jupyter Labs...\n")
    pip.main(["install", "--user", "jupyterlab"]) #os.system('cmd /k "py -m jupyterlab"') opens jupyter lab
    print()

    print("Installing Jupyter Books...\n")
    pip.main(["install", "--user", "jupyter-book"])
    print()

    os.system('cmd /k "jb --help"')

    ###########################################################################################################

    

else:

    print("First time set up already done\n\n")
