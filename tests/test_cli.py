import unittest
import mock
import StringIO
import sys
import cmd2

import mtgdb.cli.command

_LIST_PROMPT = "list>"

class CmdTest(unittest.TestCase):

    def setUp(self):
        self.input = mock.MagicMock(spec=sys.stdin)
        self.output = mock.MagicMock(spec=sys.stdout)

    def _last_write(self, nr=None):
        if nr is None:
            return self.output.write.call_args[0][0]
        return "".join(map(lambda c: c[0][0], self.output.write.call_args[-nr:]))


class CliTest(CmdTest):
    pass

    # def test_mainListCommandShouldStartAListSubCommand(self, m_listcmd):
    #     app = mtgdb.cli.command.Application(input=self.input, output=self.output)
    #     m_listcmd.return_value = mock.MagicMock()
    #
    #     self.assertFalse(app.onecmd("list"),"command should not exit after starting")
    #     self.assertTrue(m_listcmd.return_value.cmdloop.called, "command loop not called")


class ListCmdTest(CmdTest):
    pass

    # def test_shouldListInformativePromptWhenStarted(self):
    #     self.assertTrue(False, "Not implemented")
    #
    # def test_shouldHaveAnIntuitivePromptText(self):
    #     self.assertTrue(False, "Not implemented")
    #
    # def test_shouldSendViewAllOfficialSetsOnListCommand(self):
    #     self.assertTrue(False, "Not implemented")
    #
    # def test_shouldSendViewAllOfficialSetsOnEmptyLine(self):
    #     self.assertTrue(False, "Not implemented")








def suite():
    test_classes = [
        CliTest,
        ListCmdTest,
    ]
    suite = unittest.TestSuite()
    for test_class in test_classes:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(test_class))
    return suite

if __name__ == '__main__':
    unittest.main()