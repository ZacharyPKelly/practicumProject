#IMPORTS
import os
from configparser import ConfigParser

###### Creating File Folder System ########################################################################
###########################################################################################################

###### Creating File Folder System ########################################################################

parent_dir = os.path.expanduser('~')
parent_dir = parent_dir + "\OneDrive\Documents"
owd = os.getcwd() #original working directory

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

###########################################################################################################

###### Creating Config File ###############################################################################

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

###########################################################################################################