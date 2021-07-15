#!/usr/bin/env python3

# ========================= #
# DOWNLOADER TEST           #
# ========================= #

import unittest
from gpip.downloader import Downloader

class DownloaderTest(unittest.TestCase):

    def setUp(self):
        self.downloader = Downloader()

    def test_clone(self):

        source = "carlospomares.es"
        account = "pomaretta"

        path = self.downloader.download(
            source=source
            ,account=account
        )

        self.assertNotEqual(None,path)

if __name__ == '__main__':
    unittest.main()