import sys
sys.path += ['/Users/bvsc/Dropbox/Projects/Valet2']

import valet as valet
from valet import actions as a
from valet import conditions as c
from datetime import datetime

@valet.rule
def move_jpg(path):
	if c.extension_in(path, ['jpg']):
		a.tag(path, 'Inbox')
		a.move(path, '/Users/bvsc/Dropbox/Images/Photos/')
		a.notify('image ' + path + ' moved')
		return True

@valet.rule
def move_png(path):
	if c.extension_in(path, ['png']):
		a.tag(path, 'Inbox')
		a.move(path, '/Users/bvsc/Dropbox/Images/Found/')
		a.notify('image ' + path + ' moved')
		return True

@valet.rule
def move_movies(path):
	if c.extension_in(path, ['mp4']):
		a.tag(path, 'Inbox')
		a.move(path, '/Users/bvsc/Dropbox/Images/Photos/')
		a.notify('movie ' + path + ' moved')
		return True


@valet.rule
def move_pdfs(path):
	if c.extension_in(path, ['pdf']):
		a.tag(path, 'Inbox')
		a.move(path, '/Users/bvsc/Dropbox/Notes')
		a.notify('pdf ' + path + ' moved')
		return True


valet.run('/Users/bvsc/Dropbox/Camera Uploads')