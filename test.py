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

# GITHUB_CLI_VERSION = '$(curl -s "https://api.github.com/repos/cli/cli/releases/latest" | grep -Po ' + "'" + '"tag_name": "v\K[0-9.]+' + "')"
# print()
# print(GITHUB_CLI_VERSION)
# print()
# print('"https://github.com/cli/cli/releases/latest/download/gh_' + GITHUB_CLI_VERSION + '_linux_armv6.deb"')

# test = "'" + '"tag_name": "v\K[0-9.]+' + "'"
# print(test)

# checkStatus = subprocess.Popen(["gh auth status"], stderr=subprocess.PIPE)
# checkStatusOutput = checkStatus.communicate()

# print(checkStatusOutput)

is_windows = hasattr(sys, 'getwindowsversion')

print()
print('-------------------------------------------------------------\n')
print(os.name)
print(platform.release())
print()
print('-------------------------------------------------------------')