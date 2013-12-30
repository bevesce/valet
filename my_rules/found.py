import sys
sys.path += ['/Users/bvsc/Dropbox/Projects/Valet2']

import valet as valet
from valet import actions as a
from valet import conditions as c

import os
from datetime import datetime


@valet.rule
def move_images(path):
	if c.extension_in(path, c.image_extensions):
		photoPath = path
		cdate = datetime.utcfromtimestamp(os.path.getmtime(photoPath))
		imgDir = '/Users/bvsc/Dropbox/Images/Found/{year:04d}/{year:04d}-{month:02d}/'.format(year=cdate.year, month=cdate.month)
		a.move(photoPath, imgDir)
		return True

valet.run('/Users/bvsc/Dropbox/Images/Found/')