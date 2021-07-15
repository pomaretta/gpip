#!/usr/bin/env python3

# ========================= #
# INSTALL TEST              #
# ========================= #

import unittest
from gpip.downloader import Downloader
from gpip.installer import Installer
from gpip.builder import Builder

class InstallTest(unittest.TestCase):
    
    def setUp(self):
        self.downloader = Downloader()
        self.installer = Installer()
        self.builder = Builder()
        
        self.source = "tutorial-pip-package"
        self.account = "MichaelKim0407"
        
        self.path: str
        self.package: str
        self.name: str

    def step_1_clone(self):
        self.path = self.downloader.download(
            source=self.source,
            account=self.account,
            https=True
        )
        self.assertNotEqual(None,self.path)
    
    def step_2_build(self):
        self.package, self.name = self.builder.build(
            path=self.path
        )
    
    def step_3_install(self):
        r = self.installer.install(
            path=self.package,
            name=self.name
        )
        self.assertTrue(r)

    def _steps(self):
        for name in dir(self):
            if name.startswith("step"):
                yield name, getattr(self,name)
                
    def test_sequence(self):
        for name, step in self._steps():
            try:
                step()
            except Exception as e:
                self.fail("{} Failed ({}: {})".format(step,type(e),e))

if __name__ == "__main__":
    unittest.main()