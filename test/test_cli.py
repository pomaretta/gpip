#!/usr/bin/env python3

# ========================= #
# CLI TEST                  #
# ========================= #

import unittest
import os

class CliTest(unittest.TestCase):

    def test_install(self):
        file = "echo github.com/MichaelKim0407/tutorial-pip-package#my-pip-package > requirements-gpip.txt"
        command = "gpip install ./requirements-gpip.txt --https --debug"
        self.assertEqual(0,os.system(file))
        self.assertEqual(0,os.system(command))

    def test_get(self):
        command = "gpip get github.com/MichaelKim0407/tutorial-pip-package#my-pip-package --https --debug"
        self.assertEqual(0,os.system(command))

if __name__ == '__main__':
    unittest.main()