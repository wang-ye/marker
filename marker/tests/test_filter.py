from marker.filter import filter_commands
from marker.command import Command
import unittest


class FilterTest(unittest.TestCase):
    def setUp(self):
        cmd1 = Command('marker_cmd', alias='marker', description='test mark commands')
        cmd2 = Command('painter_cmd', alias='painter', description='mark commands')
        cmd3 = Command('drawer_cmd', alias='drawer', description='markdrawer commands')
        self.cmds = [cmd1, cmd2, cmd3]

    def test_filter_commands_alias(self):
        assert filter_commands(self.cmds, 'paint') == [self.cmds[1]]


    def test_filter_with_desp(self):
        assert filter_commands(self.cmds, 'markdrawer') == [self.cmds[2]]


    def test_filter_empty_result(self):
        assert filter_commands(self.cmds, 'print') == []
