import sys
sys.path += ['/Users/bvsc/Dropbox/Projects/Valet2']

import valet as valet
from valet import actions as a
from valet import conditions as c

@valet.rule
def move_images(path):
	if c.extension_in(path, c.image_extensions):
		a.tag(path, ['img:Found', 'Inbox'])
		a.move(path, '/Users/bvsc/Dropbox/Images')
		a.notify('image ' + path + ' moved')


valet.run('/Users/bvsc/Dropbox/Camera Uploads')