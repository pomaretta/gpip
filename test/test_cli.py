#!/usr/bin/env python3

# ========================= #
# CLI TEST                  #
# ========================= #

import unittest
import os

class CliTest(unittest.TestCase):

    def test_target(self):
        file = "echo 'github.com/MichaelKim0407/tutorial-pip-package:my-pip-package https=true' > requirements-gpip.txt"
        command = "mkdir deps && gpip install ./requirements-gpip.txt --debug --user --target ./deps"
        self.assertEqual(0,os.system(file))
        self.assertEqual(0,os.system(command))

    def test_install(self):
        file = "echo 'github.com/MichaelKim0407/tutorial-pip-package:my-pip-package https=true' > requirements-gpip.txt"
        command = "gpip install ./requirements-gpip.txt --debug --user"
        self.assertEqual(0,os.system(file))
        self.assertEqual(0,os.system(command))

    def test_get(self):
        command = "gpip get github.com/MichaelKim0407/tutorial-pip-package:my-pip-package --https --debug"
        self.assertEqual(0,os.system(command))

    def test_get_fail(self):
        command = "gpip get github/MichaelKim0407/tutorial-pip-package:my-pip-package --https --debug"
        self.assertNotEqual(0,os.system(command))

if __name__ == '__main__':
    unittest.main()