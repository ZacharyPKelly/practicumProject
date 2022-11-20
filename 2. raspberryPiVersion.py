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

#11211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11211

###########################################################################################################
#Installing Dependencies
###########################################################################################################

required  = {'gitpython', 'jupyterlab', 'jupyter-book', 'nbconvert[webpdf]'} 
installed = {pkg.key for pkg in pkg_resources.working_set}
missing   = required - installed

if missing:
    #implementing pip as a subprocess:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

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

    print('Installing GitHubs CLI...\n')

    os.chdir(jupyterDirectory)

    gitHubCliInstallation = open(r'installGitHubCli.sh', 'w+')
    gitHubCliInstallation.write('#!/bin/bash\n')
    gitHubCliInstallation.write('GITHUB_CLI_VERSION=$(curl -s "https://api.github.com/repos/cli/cli/releases/latest" | grep -Po \'"tag_name": "v\K[0-9.]+\')\n')
    gitHubCliInstallation.write('curl -Lo gh.deb "https://github.com/cli/cli/releases/latest/download/gh_${GITHUB_CLI_VERSION}_linux_armv6.deb"\n')
    gitHubCliInstallation.write('sudo dpkg -i gh.deb\n')
    gitHubCliInstallation.write('rm -rf gh.deb')
    gitHubCliInstallation.close()

    filePermission = subprocess.Popen(['sudo', 'chmod', '+x', 'installGitHubCli.sh'])
    filePermission.communicate()

    subprocess.call('./installGitHubCli.sh')

    os.remove(os.path.join(jupyterDirectory, "installGitHubCli.sh"))

    print()
    print('GitHubs CLI installed!\n')

    ###########################################################################################################
    #Creating Config File
    ###########################################################################################################

    print("Creating configuration file...\n")

    print("In order to clone the Eswatini repository, you will need a Github Account along with your username and Personal Access Token (PAT)")
    print("You can generate a PAT by going to:")
    print("Github Account Settings (Click on your profile icon in top right corner of github and select settings at the bottom of the menu that pops up)")
    print("Developer Settings (Found at the bottom of the list of options on the left hand side of the page)")
    print("Personal Access Tokens (Found at the bottom of the list of options on the left hand side of the page)")
    print("Generate New Token (Found center-right near the top of the page)")
    print("Give your PAT a descriptive name, set the expiration date to be 'No Expiration' and check off 'REPO', 'WRITE:PACKAGES', 'USER', and 'READ:ORG' (found under ADMIN:ORG)")
    print("Select Generate Token at the bottom of your page and copy the token into your clip board\n")

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
    print()
    print("Configuration file created!\n")

    ###########################################################################################################
    #Logging User into Github using CLI
    ###########################################################################################################
    
    print("Logging into GitHub...\n")

    loggedOutMessage = (None, b'You are not logged into any GitHub hosts. Run \x1b[0;1;39mgh auth login\x1b[0m to authenticate.\n')

    checkStatus = subprocess.Popen(['gh', 'auth', 'status'], stderr=subprocess.PIPE)
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