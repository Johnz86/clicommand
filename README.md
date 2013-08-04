clicommand
==========

Dispatch function decorator for python docopt library

.. code:: python

    from clicommand import Cli
	from docopt import docopt

.. code:: python

    cli = Cli(docopt(__doc__))

``Cli`` takes result of docopt library as mandatory argument:

.. code:: python

    @cli.command({'key':function,'key':type,'key':'exactString'})
    def normalFunction(arguments):
  		print 'matched pattern',arguments

