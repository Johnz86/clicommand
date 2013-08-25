"""Function decorator dispatcher for docopt command line interface.

 * Repository and issue-tracker: https://github.com/Johnz86/clicommand
 * Licensed under terms of MIT license (see LICENSE-MIT)
 * Copyright (c) 2013 Jan Jakubcik, jakubcikjan@gmail.com

"""

import os
from inspect import isfunction,ismethod
from types import TypeType

__version__ = '0.3'

class Cli:
    '''Command dispatcher for docopt command line interface'''
    def __init__( self, data ):
        self._docoptdata = data
        self._optimaldata = {key:value for key,value in self._docoptdata.items() if value!=False and value!=None }

    def command( self, *args, **kwargs ):
        return CommandDispatcher( self, *args, **kwargs )
        
    def onStart( self ):
        pass
        
    def onExit( self ):
        pass

class CommandDispatcher:
    '''Dispatcher of functions '''
    def __init__( self, cli_decorator, *positional, **keywords ):
        self._cli_decorator = cli_decorator
        if keywords:
            decoratorArgs = keywords
        elif type(positional[0]) is dict:
            decoratorArgs = positional[0]
        else: 
            decoratorArgs = None
            print 'cli has incorrect arguments',positional[0]
            exit(1)
        self.decArgs = decoratorArgs

    def __call__( self, f ):
        self._f = f
        if(self.matchCommand(self._cli_decorator._docoptdata,self.decArgs)):
            self.wrap(self._cli_decorator._docoptdata)
        return self.wrap

    def wrap( self, *args, **kwargs ):
        self._cli_decorator.onStart()
        function = self._f( *args, **kwargs )   
        self._cli_decorator.onExit()
        return function

    def matchCommand(self,argumentlist,commandlist):
        for key,value in commandlist.items():
            if(argumentlist.has_key(key)):
                if(not self.compareAguments(argumentlist[key],value)):
                    return False
            else:
                return False
        if any([key for key in self._cli_decorator._optimaldata.keys() if key not in commandlist.keys()]):
            return False
        else:
            return True

    def compareAguments(self,compareArg,commandArg):
        if(compareArg == commandArg):
            return True
        elif(commandArg == '?'):
            return True
        elif(type(commandArg) is bool or commandArg is None or compareArg is None):
            return False
        elif(type(commandArg) is type):
            if commandArg is str:
                return True
            elif(commandArg is int and str.isdigit(compareArg)):
                return True
            else:
                return False
        if type(commandArg) in (list, tuple, set, frozenset):
            for choice in commandArg:
                if self.compareAguments(compareArg,choice):
                    return True
            return False
        elif callable(commandArg):
            if(commandArg(compareArg)):
                return True
            else: 
                return False
        else:
            return False
