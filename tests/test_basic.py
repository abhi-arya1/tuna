"""

Generic Tests for Tuna CLI

"""

# pylint: disable=missing-module-docstring, missing-function-docstring, missing-class-docstring, line-too-long

import unittest
from utils import mock_stdout, mock_argv
from tuna.cli.main import main

class TestTunaCLI(unittest.TestCase):

    def test_help(self):
        with mock_argv('tuna', '--help'), mock_stdout() as mock_out:
            with self.assertRaises(SystemExit):
                main()
            output = mock_out.getvalue()
            self.assertIn('Usage:', output)

    def test_version(self):
        with mock_argv('tuna', '--version'), mock_stdout() as mock_out:
            with self.assertRaises(SystemExit):
                main()
            output = mock_out.getvalue()
            self.assertIn('Tuna v', output)

if __name__ == '__main__':
    unittest.main()
