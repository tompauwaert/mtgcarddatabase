import sys
import cmd2
from cmd2 import options
from cmd2 import make_option
from tabulate import tabulate


import core.data_view
import core.database
import data
from core.data_labels import SET_LABELS

class Application(cmd2.Cmd):
    """
    Starts the CLI interface for the application.
    """

    def __init__(self, debug, input=sys.stdin, output=sys.stdout):
        cmd2.Cmd.__init__(self, stdin=input, stdout=output)
        self._debug = debug
        self.prompt = 'mtgdb> '

    #
    # LISTING
    #

    @options([make_option('-r', '--remote', action="store_true",
                          help="allow remote fetching of data")])
    def do_list(self, arg, opts=None):
        """
        List a number of mtg sets. Use a parameter to specify
        which sets to list. Defaults to all available sets.

        Parameters:
        - available: list all sets that are currently available for download


        - second parameter may be given as remote
        """
        remote = False
        if opts.remote:
            remote = True

        if arg == '':
            self._list_available(remote=remote)
        elif arg == "available":
            self._list_available(remote=remote)

        return False


    def _list_available(self, remote=False):
        data_view = core.data_view.DataView()
        available_sets = data_view.available_sets(remote=remote)

        # sort based on release date, descending.
        def get_set_release_date(item):
            return item[SET_LABELS.RELEASE_DATE]

        available_sets.sort(reverse=True, key=get_set_release_date)

        # data preprocessed for tabulating
        print(tabulate(available_sets, headers='keys', tablefmt='orgtbl'))

    #
    # DATA
    #

    def do_data(self, arg):
        """
        Enters data maintenance mode. You can use this to clear your cache,
        or if you are in debug mode this allows you to inspect the data.

        In order to clear the cache following parameter:
        -clear-cache

        If you wish to enter inspection mode use following parameter:
        -inspect

        """

        if arg == "-clear-cache":
            database = core.database.Database()
            database.clear_cache()

        elif arg == "-inspect":
            if self._debug:
                data_cmd = data.DataInspection()
                data_cmd.cmdloop()
            else:
                print "You must be in debug mode to run data inspection."






















