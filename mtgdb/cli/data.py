from cmd2 import Cmd
from cmd2 import options
from cmd2 import make_option
from tabulate import tabulate

import core.data_view
from core.data_labels import SET_LABELS

class DataInspection(Cmd):
    """
    Class that implements the commands to inspect data
    This is only available in debug mode.
    """

    def __init__(self):
        Cmd.__init__(self)
        self.prompt = "inspect> "

