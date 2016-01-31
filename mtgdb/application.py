"""
Start the application.

At this point this starts the CLI, because there is only
one interface available.
"""


import sys
import cli.command

if __name__ == "__main__":

    debug = False
    for arg in sys.argv:
        if arg == '--debug':
            debug = True

    if debug:
        sys.argv.remove('--debug')

    app = cli.command.Application(debug)
    app.cmdloop()
