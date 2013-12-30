import sys
sys.path += ['/Users/bvsc/Dropbox/Projects/Valet2']

import os
import re
import valet
from valet import actions as a
from valet import conditions as c


@valet.rule
def inbox_tag(path):
	a.tag(path, 'Inbox')

@valet.rule
def move_images(path):
	if c.extension_in(path, c.image_extensions):
		a.tag(path, 'Inbox')
		a.move(path, '/Users/bvsc/Dropbox/Images')
		a.notify('image ' + path.split('/')[-1] + ' moved')
		return True

def replf(g):
	return g.group(1)

year_pattern = re.compile(r'[\(\[](\d\d\d\d)[\)\]]')

def cleanup_movie_file_name(path):
	filename = '.'.join(path.split('/')[-1].split('.')[0:-1])
	filename = filename.replace('.', ' ')
	filename = filename.replace('_', ' ')
	filename = filename.replace('-', ' ')
	year = year_pattern.findall(filename)
	if year:
		year = year[0]
	filename = year_pattern.split(filename)[0]
	if filename.startswith('the') or filename.startswith('The'):
		filename = filename[4:] + ', The'
	if year:
		filename = filename.strip() + ' ' + year
	return filename



@valet.rule
def move_movies(path):
	if c.extension_in(path, c.movie_extensions):
		folder_name = cleanup_movie_file_name(path)
		a.tag(path, 'Inbox')
		a.move(path, '/Users/bvsc/Movies/' + folder_name)
		a.notify(path.split('/')[-1], url='file:///Users/bvsc/Movies/' + folder_name + '/' + path.split('/')[-1])
		return True


@valet.rule
def open_trash_orange_invoice(path):
	if c.any_where_froms_starts_with(path, 'https://www.orange.pl/gear/ecare/invoices/invoicedocumentexportservlet'):
		a.open(path)

# @valet.rule
# def tag_uw(path):
# 	if c.any_where_froms_constains(path, 'mimuw'):
# 		a.tag(parh, 'p:UW')

@valet.rule
def move_books(path):
	if c.extension_in(path, c.book_extensions):
		a.tag(path, 'Inbox')
		a.move(path, '/Users/bvsc/Dropbox/Library')
		a.notify('book ' + path.split('/')[-1] + ' moved')
		return True

@valet.rule
def move_inside_folder(path):
	if c.is_dir(path):
		a.tag(path, 'Inbox')
		valet.run_rules(path, [move_movies, move_books])
		return True

valet.run('/Users/bvsc/Downloads')