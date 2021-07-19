#!/usr/bin/env python3

# ========================= #
# OPTIMIZE TEST             #
# ========================= #

from gpip import get
import time
import os

if __name__ == '__main__':

    print("Vanilla install time")

    start = time.time()

    os.system("git clone https://www.github.com/MichaelKim0407/tutorial-pip-package > /dev/null 2>&1")
    os.chdir('./tutorial-pip-package')
    os.system("python3 setup.py bdist_wheel > /dev/null 2>&1")
    wheel_dist = os.listdir('dist')[0]
    os.system("pip3 install {} > /dev/null 2>&1".format(os.path.join('dist', wheel_dist)))
    
    stop = time.time()

    print(f"{'{:.4f}'.format(stop - start)}s\n")

    print("Get install time")

    start = time.time()

    get(
        "github.com/MichaelKim0407/tutorial-pip-package#name=my-pip-package;force=true;https=true"
        ,debug=True
    )

    stop = time.time()

    print(f"{'{:.4f}'.format(stop - start)}s")