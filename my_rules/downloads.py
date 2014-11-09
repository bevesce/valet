import os
import sys

sys.path += [os.path.expanduser('~/Dropbox/Projects/Valet2')]
import valet


class Inbox(valet.Rule):
    def when(self):
        return not self.has_tag('Inbox')

    def what(self):
        self.tag('Inbox')


class Movie(valet.Rule):
    def when(self):
        return self.is_movie()

    def what(self):
        self.move('~/Movies')


class Image(valet.Rule):
    def when(self):
        return self.is_image()

    def what(self):
        self.add_ctimestamp()
        self.move(
            '~/Dropbox/Images/Found/Found {}'.format(
                self.get_cdate().strftime('%Y-%m')
            )
        )


class Books(valet.Rule):
    def when(self):
        return self.is_book()

    def what(self):
        self.move('~/Dropbox/Books')


class Comics(valet.Rule):
    def when(self):
        return self.is_comic()

    def what(self):
        self.move('~/Dropbox/Books/Comics')


class Dirs(valet.Rule):
    def when(self):
        return self.is_dir()

    def what(self):
        valet.run_rules(self.fullpath)


valet.run('~/Downloads')
