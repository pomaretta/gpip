#!/usr/bin/env python3

# ========================= #
# DOWNLOADER TEST           #
# ========================= #

import unittest
from gpip._internal.downloader import Downloader

class DownloaderTest(unittest.TestCase):

    def setUp(self):
        self.downloader = Downloader()

    def test_clone(self):

        source = "carlospomares.es"
        account = "pomaretta"

        path = self.downloader.download(
            source=source
            ,account=account
            ,https=True
            ,debug=True
        )

        self.assertNotEqual(None,path)
        self.assertTrue("carlospomares.es" in path)

if __name__ == '__main__':
    unittest.main()