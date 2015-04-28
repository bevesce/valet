import os
import sys

sys.path += [os.path.expanduser('~/Dropbox/Projects/Valet2')]
import valet


class RuleName(valet.Rule):
    def when(self):
        pass

    def then(self):
        pass

valet.run('path/to/run/on')
