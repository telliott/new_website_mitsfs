#!/usr/bin/python3
import shutil

# For now a super simple script to get the dex into place. Eventually should grab
# it from the db directly

source = "dex.txt"
destination = "../pinkdex/dexPlainText.txt"
shutil.copyfile(source, destination)


