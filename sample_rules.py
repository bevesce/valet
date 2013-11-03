import os
import valet
from valet import actions as a
from valet import conditions as c


@valet.rule()
def move_images(path):
	if c.extension_in(path, c.image_extensions):
		a.move(path, os.path.expanduser('~/Pictures'))


@valet.rule()
def move_movies(path):
	if c.extension_in(path, c.movie_extensions):
		a.tag(path, 'to_watch')
		a.move(path, os.path.expanduser('~/Movies'))


valet.run('~/Downloads')