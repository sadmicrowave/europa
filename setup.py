#!/usr/local/bin/python3

# A simple setup script to create an executable using PyQt4. This also
# demonstrates the method for creating a Windows executable that does not have
# an associated console.
#
# PyQt4app.py is a very simple type of PyQt4 application
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the application

application_title = "game" #what you want to application to be called
main_python_file = "game.py" #the name of the python file you use to run the program

import sys, py2exe
from distutils.core import setup

setup(
    windows=[{ 'script':'game.py'
              ,'icon_resources': [(1, 'game_icon.ico')]
              ,'dest_base' : 'The Europa Protocol'
            }]
    ,data_files = [('', ['world.xlsx', 'map.xlsx', 'map.txt', 'game_icon.ico'])]
      

      )
