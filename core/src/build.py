import sys

import PyInstaller.__main__

args = [
    "--onefile",
    "installer.py",
]

PyInstaller.__main__.run(args)
