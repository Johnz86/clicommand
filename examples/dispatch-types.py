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

if __name__ == '__main__':

    cli = Cli(docopt(__doc__))

#int means, that provided string is a number
@cli.command({'FOLDER':os.path.isdir,'--count':int})
def getCount(arguments):
  print 'getCount',arguments

#object means attribute is optional.
@cli.command({'FOLDER':os.path.isdir,'--count':'?'})
def getFolder(arguments):
  print 'getFolder',arguments

#check if --file has value True
@cli.command({'FOLDER':os.path.isdir,'--file':True})
def getFile(arguments):
  print 'getFile',arguments

#checks if AGREE has value of yes|no|ignore
@cli.command({'FOLDER':str,'AGREE':['yes','no','ignore']})
def folderAgreed(arguments):
  print 'folderAgreed',arguments