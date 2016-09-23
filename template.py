import os
import sys

sys.path += [os.path.expanduser('~/path/to/valet')]
import valet


class RuleName(valet.Rule):
    def when(self):
        pass

    def then(self):
        pass

valet.run('path/to/run/on')
