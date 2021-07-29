#!/usr/bin/env python3

# ========================= #
# REPOSITORY TEST           #
# ========================= #

import unittest
from gpip._internal.repository import Repository

class RepositoryTest(unittest.TestCase):
    
    def setUp(self):
        self.repository = Repository(
            url="github.com/MichaelKim0407/tutorial-pip-package:my-pip-package",
            https=True,
            force=True,
            debug=True
        )
    
    def test_install(self):
        self.repository.install()
        self.assertTrue(self.repository.__exists__())
    
if __name__ == '__main__':
    unittest.main()