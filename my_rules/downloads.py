import sys
sys.path += ['/Users/bvsc/Dropbox/Projects/Valet2']

import os
import valet
from valet import actions as a
from valet import conditions as c


@valet.rule
def inbox_tag(path):
	a.tag(path, 'Inbox')

@valet.rule
def move_images(path):
	if c.extension_in(path, c.image_extensions):
		a.tag(path, 'img:Found')
		a.move(path, '/Users/bvsc/Dropbox/Images')


@valet.rule
def move_movies(path):
	if c.extension_in(path, c.movie_extensions):
		a.move(path, '/Users/bvsc/Movies')


@valet.rule
def move_books(path):
	if c.extension_in(path, c.book_extensions):
		a.move(path, '/Users/bvsc/Dropbox/Library')

@valet.rule
def move_inside_folder(path):
	if c.is_dir(path):
		valet.run_rules(path, [move_movies, move_books])

valet.run('/Users/bvsc/Downloads')