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

import git
from git import repo

###########################################################################################################
#Creating File Folder System
###########################################################################################################

parent_dir = os.path.expanduser('~')

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
# print()
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
# print()

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

    print('File Folder system created!\n')

    ###########################################################################################################
    #Installing GitHubs CLI
    ###########################################################################################################

    
    GITHUB_CLI_VERSION = subprocess.Popen(['curl', '-s', '"https://api.github.com/repos/cli/cli/releases/latest"', '|', 'grep', '-Po', "'" + '"tag_name": "v\K[0-9.]+' + "'"])
    GITHUB_CLI_VERSION = GITHUB_CLI_VERSION.communicate()

    installGitHubCLIOne = subprocess.Popen(['curl', '-Lo', 'gh.deb', '"https://github.com/cli/cli/releases/latest/download/gh_' + GITHUB_CLI_VERSION + '_linux_armv6.deb"'])
    installGitHubCLIOne.communicate()

    installGitHubCLITwo = subprocess.Popen(['sudo', 'dpkg', '-i', 'gh.deb'])
    installGitHubCLITwo.communicate()

    installGitHubCLIThree = subprocess.Popen(['rm', '-rf', 'gh.deb'])
    installGitHubCLIThree.communicate()

    #curl -Lo gh.deb "https://github.com/cli/cli/releases/latest/download/gh_${GITHUB_CLI_VERSION}_linux_armv6.deb"

    # GITHUB_CLI_VERSION1=$(curl -s "https://api.github.com/repos/cli/cli/releases/latest" | grep -Po '"tag_name": "v\K[0-9.]+')
	#         cd ~
	#         curl -Lo gh.deb "https://github.com/cli/cli/releases/latest/download/gh_${GITHUB_CLI_VERSION}_linux_armv6.deb"
	#         sudo dpkg -i gh.deb
	#         rm -rf gh.deb

    #         gitAdd = subprocess.Popen(['git', 'add', '.'])
    #             gitAdd.communicate()