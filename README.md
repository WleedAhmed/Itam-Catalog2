
# Item Catalog
_A project for Udacity Full Stack Nanodegree._

## About the project:
I was asked to to develop an application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items. 

## To Run the code:
You will need **Python**, **Vagrant** and **VirtualBox** installed on your computer. once you have them, you are ready for setup. 
[Download Vagrant here](https://www.vagrantup.com/)
[Download VirtualBox here](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)


## Setup
**1 - The VM:** 
if you don't have the folder fullstack-nanodegree-vm, use your github account to clone this file: 
[fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm)
[how to clone a file in github](https://help.github.com/articles/fork-a-repo/)
After finishing, you will have a directory called fullstack-nanodegree-vm.

**2 - Launch Vagrant VM:** 
Using your terminal, cd to the vagrant directory and run the command `vagrant up`. When `vagrant up` finishes running, log in into your VM with `vagrant ssh`.

**5 - Run these commands:**
In order to make sure you have all the needed before starting the application - run these commands first:
`sudo pip install Flask`
`sudo pip install sqlalchemy`
`sudo pip install requests`
`sudo pip install oauth2client`

**4 - The data base:** 
In the directory "project", there is already database established and filled with some default categories with films. However, if you want to restore these default values anytime you can simply delete the files **movies.db** and **database_setup.pyc** then run these commands through your terminal:
`python database_setup.py` to establish the DB skeleton.
`python movies.py` to fill in the DB with the default values.

**5- To execute the program:** 
Through your terminal run the command `python application.py`. Then navigate via your browser to [http://localhost:8000/](http://localhost:8000/)
