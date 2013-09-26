"""Function decorator dispatcher for docopt command line interface.

 * Repository and issue-tracker: https://github.com/Johnz86/clicommand
 * Licensed under terms of MIT license (see LICENSE-MIT)
 * Copyright (c) 2013 Jan Jakubcik, jakubcikjan@gmail.com

"""

__version__ = '0.4'

class Cli:
    """Command dispatcher for docopt command line interface"""
    def __init__( self, data ):
        self.docoptdata = data
        self.optimaldata = {key:value for key,value in self.docoptdata.items() if value!=False and value is not None}

    def command( self, *args, **kwargs ):
        return CommandDispatcher( self, *args, **kwargs )
        
    def on_start( self ):
        pass
        
    def on_exit( self ):
        pass

class CommandDispatcher:
    """Dispatcher of functions """
    def __init__( self, cli_decorator, *positional, **keywords ):
        self._cli_decorator = cli_decorator
        if keywords:
            decorator_args = keywords
        elif type(positional[0]) is dict:
            decorator_args = positional[0]
        else: 
            decorator_args = None
            print 'cli has incorrect arguments',positional[0]
            exit(1)
        self.dec_args = decorator_args

    def __call__( self, f ):
        self._f = f
        if self.match_command(self._cli_decorator.docoptdata,self.dec_args):
            self.wrap(self._cli_decorator.docoptdata)
        return self.wrap

    def wrap( self, *args, **kwargs ):
        self._cli_decorator.on_start()
        function = self._f( *args, **kwargs )   
        self._cli_decorator.on_exit()
        return function

    def match_command(self,argumentlist,commandlist):
        for key,value in commandlist.items():
            if argumentlist.has_key(key):
                if not self.compare_commands(argumentlist[key],value):
                    return False
            else:
                return False
        if any([key for key in self._cli_decorator.optimaldata.keys() if key not in commandlist.keys()]):
            return False
        else:
            return True

    def compare_commands(self,compare_arg,command_arg):
        if compare_arg == command_arg:
            return True
        elif command_arg == '?':
            return True
        elif type(command_arg) is bool or command_arg is None or compare_arg is None:
            return False
        elif type(command_arg) is type:
            if command_arg is str:
                return True
            elif command_arg is int and str.isdigit(compare_arg):
                return True
            else:
                return False
        if type(command_arg) in (list, tuple, set, frozenset):
            for choice in command_arg:
                if self.compare_commands(compare_arg,choice):
                    return True
            return False
        elif callable(command_arg):
            if command_arg(compare_arg):
                return True
            else: 
                return False
        else:
            return False
