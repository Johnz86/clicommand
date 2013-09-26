"""Usage: dispatch-types.py FOLDER [options] [AGREE]

Arguments:
  FOLDER     folder name
  AGREE      yes|no|ignore
Options:
  --count=N   number of files
  --file      file is present
"""
import os
from clicommand import Cli
from docopt import docopt

def command_start(message):
        print 'On start',message
        
def command_exit(message):
        print 'On exit',message

if __name__ == '__main__':

    cli = Cli(docopt(__doc__))
    cli.on_start=lambda:command_start('Hello')
    cli.on_exit=lambda:command_exit('Bye')

#int means, that provided string is a number
@cli.command({'FOLDER':os.path.isdir,'--count':int})
def get_count(arguments):
  print 'get_count executed',arguments

#object means attribute is optional.
@cli.command({'FOLDER':os.path.isdir,'--count':'?'})
def get_folder(arguments):
  print 'get_folder executed',arguments

#check if --file has value True
@cli.command({'FOLDER':os.path.isdir,'--file':True})
def get_file(arguments):
  print 'get_file executed',arguments

#checks if AGREE has value of yes|no|ignore
@cli.command({'FOLDER':os.path.isdir,'AGREE':['yes','no','ignore']})
def folder_agreed(arguments):
  print 'folder_agreed executed',arguments
