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
		a.notify('image ' + path.split('/')[-1] + ' moved')


@valet.rule
def move_movies(path):
	if c.extension_in(path, c.movie_extensions):
		a.tag(path, 'Inbox')
		a.move(path, '/Users/bvsc/Movies')
		a.notify(path.split('/')[-1], url='file:///Users/bvsc/Movies/' + path.split('/')[-1])


@valet.rule
def open_trash_orange_invoice(path):
	if c.any_where_froms_starts_with(path, 'https://www.orange.pl/gear/ecare/invoices/invoicedocumentexportservlet'):
		a.open(path)


@valet.rule
def move_books(path):
	if c.extension_in(path, c.book_extensions):
		a.tag(path, 'Inbox')
		a.move(path, '/Users/bvsc/Dropbox/Library')
		a.notify('book ' + path.split('/')[-1] + ' moved')

@valet.rule
def move_inside_folder(path):
	if c.is_dir(path):
		a.tag(path, 'Inbox')
		valet.run_rules(path, [move_movies, move_books])

valet.run('/Users/bvsc/Downloads')