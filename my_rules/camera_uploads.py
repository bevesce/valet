import sys
import os
sys.path += [os.path.expanduser('~/Dropbox/Projects/Valet2')]
import valet


class ImageOrMovie(valet.Rule):
    def when(self):
        return self.is_image() or self.is_movie()

    def what(self):
        self.tag('Inbox')
        self.add_ctimestamp()
        self.move(
            '~/Dropbox/Images/Photos/Photos {}'.format(
                self.get_cdate().strftime('%Y-%m')
            )
        )


valet.run('~/Dropbox/Camera Uploads')
