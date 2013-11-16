"""Find duplicates of image files by hash"""

import hashlib
import os

def getmd5(data):
    md5 = hashlib.md5(data)
    return md5.digest()

class CopyFinder(object):
    def __init__(self):
        self.imghashes = {}
        self.exts = ('.jpeg', '.jpg', '.png', '.tif')

    def findcopies(self, fpath):
        """Return (md5, copies) where copies is a list of fnames"""
        with open(fpath, 'rb') as f:
            md5 = getmd5(f.read())
        if md5 in self.imghashes:
            copies = self.imghashes[md5]
            copies.append(fpath)
            return md5, copies
        else:
            self.imghashes[md5] = [fpath]
            return None

    def find(self, directory):
        copygroups = {}
        for root, subFolders, files in os.walk(directory):
            for fname in files:
                fpath = os.path.join(root, fname)
                ext = os.path.splitext(fname)[1]
                if ext in self.exts:
                    stuff = self.findcopies(fpath)
                    if stuff:
                        md5, copies = stuff
                        copygroups[md5] = copies
        return copygroups

def test_copyfinder():
    directory = raw_input("Directory to search recursively for duplicates: ")
    finder = CopyFinder()
    copydata = finder.find(directory)
    for copygroup in copydata.values():
        print("==These are the same==")
        for copy in copygroup:
            print(copy)
        print("")

if __name__ == '__main__':
    test_copyfinder()
