import sys
import cmd2
from tabulate import tabulate


import core.data_view
from core.data_labels import SET_LABELS

class Application(cmd2.Cmd):
    """
    Starts the CLI interface for the application.
    """

    def __init__(self, debug, input=sys.stdin, output=sys.stdout):
        cmd2.Cmd.__init__(self, stdin=input, stdout=output)
        self._debug = debug
        self.prompt = 'mtgdb> '

    def do_list(self, arg):
        """
        List a number of mtg sets. Use a parameter to specify
        which sets to list. Defaults to all available sets.

        Parameters:
        - available: list all sets that are currently available for download

        """
        if arg is None:
            self._list_available()
        elif arg == "available":
            self._list_available()

        return False


    def _list_available(self):
        data_view = core.data_view.DataView()
        available_sets = data_view.available_sets()

        # sort based on release date, descending.
        def get_set_release_date(item):
            return item[SET_LABELS.RELEASE_DATE]

        available_sets.sort(reverse=True, key=get_set_release_date)

        # data preprocessed for tabulating
        print(tabulate(available_sets, headers='keys', tablefmt='orgtbl'))

























