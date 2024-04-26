# -*- coding: utf-8 -*-

import os

ret = os.system("pyside6-rcc resources.qrc -o ../../shmtu_auth/src/gui/resource/resources.py")

if ret != 0:
    print("Failed!")
    exit(1)

print("Done!")
