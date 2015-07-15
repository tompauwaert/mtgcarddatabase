import cmd2
import sys

class Application(cmd2.Cmd):

    def __init__(self, input=sys.stdin, output=sys.stdout):
        cmd2.Cmd.__init__(self, stdin=input, stdout=output)

    def do_list(self, arg):
        listcmd = ListCmd()
        listcmd.cmdloop()
        return False


class ListCmd(cmd2.Cmd):

    _PROMPT = "list>"

    def __init__(self, input=sys.stdin, output=sys.stdout):
        Application.__init__(input, output)
        self.prompt = self._PROMPT


