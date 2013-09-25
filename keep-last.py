#!/usr/bin/python
import sys
import getopt
import os
from os import listdir
from os.path import isfile, join

class RunException(Exception):
    def __init__(self, msg):
        self.msg = msg

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


class Keeper():
    def load(self, directory):
        self.files = [ f for f in listdir(directory) if isfile(join(directory,f)) ]


def main(argv=None):

    if argv is None:
        argv = sys.argv
  
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help", "directory="])
        except getopt.error, msg:
            raise Usage(msg)

        for o, a in opts:
            if o in ("-h", "--help"):
                raise Usage("""Usage:
%s [--help]""" % os.path.basename(sys.argv[0]))
            elif o in ("--directory"):
                directory = a

        if not "directory" in locals():
            raise Usage("missing parameter --directory")
        if not os.path.isdir(directory):
            raise Usage("directory %s cannot be found" % directory)

        keeper = Keeper()
        keeper.load(directory)
        print keeper.files

    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())
