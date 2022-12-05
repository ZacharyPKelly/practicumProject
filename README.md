# Jupyter Uploader

This program was created to help ease the process of uploading Jupyter Books and Jupyter Notebooks to the University of Eswatini's Jupyter repository website.

There are several requirements for running this program:

1. You will need git installed on your computer. You can find the link to download Git for your computer [here](https://git-scm.com/downloads).
          
2. You will need Python version >3.8 and <3.9.2, though 3.9.2 is recomended. You can find the link to download Python 3.9.2 [here](https://www.python.org/downloads/release/python-392/).

3. You will need a GitHub account, and will need to be added as a contributer with writing privlages to the Eswatini Website Repository. Please contact the moderater of the website in order to added as a contributer.

4. Next you will need to make sure your Python Scripts folder is on you PATH. You can do this easily by pressing WIN + R, typing in 'cmd' then pressing enter. You can then type in 'pip' into the Command Terminal and press enter. If you are told: 'pip is not recognized as an internal or external command, operable program or batch file' then you're Python Scripts folder is not on your PATH.

<p align="center">
  <img src="https://user-images.githubusercontent.com/92888996/205692010-32ac5eb0-5b44-450e-99e2-2c81eba6dffa.png" width="650"/>
</p>

If you are given a list of commands that you can use with pip, congratulations you can start using the program. Otherwise you will need to continue with the steps in order to add your Python Scripts folder to your PATH.

5. Open your file explorer and turn on 'Hidden items' in the 'View' tab found at the top of the explorer

<p align="center">
  <img src="https://user-images.githubusercontent.com/92888996/205693336-47b16c8c-1215-44ad-8d39-393657b8ac90.png" width="650"/>
</p>

6. Navigate to your Python Scripts folder and copy the path. This folder can found at:C:\Users\"Your Username"\AppData\Local\Programs\Python\Python39\Scripts. You can copy the path by right click on 'Scripts' and selecting 'Copy address as text'.

<p align="center">
  <img src="https://user-images.githubusercontent.com/92888996/205694490-25d0bbb6-7d31-4b1b-a57f-2b9d889184c7.png" width="650"/>
</p>

7. Open your Environment Variables. This can be done by typing 'System Variables' into your start button's search bar and selecting 'Edit the system environment variables'.

<p align="center">
  <img src="https://user-images.githubusercontent.com/92888996/205696333-3926ac17-9e8b-4ff6-bffd-93b6f12a6296.png" width="650"/>
</p>

8. Select 'Environment Variables' found in the bottom left of the System Properites window that will have opened.

<p align="center">
  <img src="https://user-images.githubusercontent.com/92888996/205697267-49a29b27-f950-4341-a838-280e01887321.png" width="650"/>
</p>

9. Select the 'PATH' line found in the 'User Variables' window at the top of the Environment Variables window that will have opened. Then press the 'Edit' button.

<p align="center">
  <img src="https://user-images.githubusercontent.com/92888996/205697890-c6255d85-6a04-496d-a87f-ce2f51bdefd0.png" width="650"/>
</p>

10. In the 'Edit environment variable' window that will have opened press new. A blank line should appear at the bottom of the list of PATH where you can now paste the Python Scripts path. You can now press 'OK' on each of three windows that will be open in order to close them out.

<p align="center">
  <img src="https://user-images.githubusercontent.com/92888996/205698498-cf23b9e5-e4b4-44b4-89fb-5741348f126f.png" width="650"/>
</p>

11. You can now test to see if your Python Scripts folder is correctly on path. Once again press 'WIN+R' and type in 'cmd' to open your command terminal. Enter 'pip' and press enter; You should see a list of commands like in the picture below.

<p align="center">
  <img src="https://user-images.githubusercontent.com/92888996/205699479-2c8159fe-9195-4712-b5be-c2e68d81998b.png" width="650"/>
</p>

## Known Issues/Bugs

-When running for the first time, if GitHubs CLI commands are being installed for the first time you may need to restart the program in order to for the GH commands to work.
