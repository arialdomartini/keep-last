#!/usr/bin/python
import sys
import getopt
import os
import re
from os import listdir
from os.path import isfile, join

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


class Keeper():
    def load(self, directory):
        self.files = [ f for f in listdir(directory) if isfile(join(directory,f)) ]

    def is_a_rev_file(self, filename):
        return re.match(".*\.rev_.[0-9]{11}", filename)

    def get_files(self):
        return [ self.group_with_oldest_revs(f) for f in self.files if not self.is_a_rev_file(f) ]

    def is_a_rev_of(self, rev_candidate, filename):
        return rev_candidate.find(filename) == 0 and self.is_a_rev_file(rev_candidate)

    def group_with_oldest_revs(self, filename):
        return {'filename' : filename, 'old_revs': sorted([ f for f in self.files if self.is_a_rev_of(f, filename) ])[:-3]}



def fake_purge(item):
    print item

def real_purge(item):
    os.remove(item)


def main(argv=None):

    if argv is None:
        argv = sys.argv
  
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help", "directory=", "show-only"])
        except getopt.error, msg:
            raise Usage(msg)

        purger = real_purge

        for o, a in opts:
            if o in ("-h", "--help"):
                raise Usage("""Usage:
%s [--help] --directory=<directory> [--show-only]""" % os.path.basename(sys.argv[0]))
            elif o in ("--directory"):
                directory = a
            elif o in ("--show-only"):
                purger = fake_purge

        if not "directory" in locals():
            raise Usage("missing parameter --directory")
        if not os.path.isdir(directory):
            raise Usage("directory %s cannot be found" % directory)

        keeper = Keeper()
        keeper.load(directory)
        for item in keeper.get_files():
            for rev in item['old_revs']:
                purger(os.path.join(directory, rev))

    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())
