# -*- coding: utf-8 -*-"""
"""
Usage:
    valet.py load
    valet.py [-h]
    valet.py

Options:
    -h --help    Show this screen
"""
from __future__ import unicode_literals
import sys
import os
import subprocess
import datetime as dt
import shutil
from functools import wraps
from itertools import chain
import docopt

import launchd
import tags
import log

DEBUG = False
logger = log.Log()


def run(dir_path):
    dir_path = os.path.expanduser(dir_path)
    logger.log('run on ' + dir_path)
    if docopt.docopt(__doc__)['load']:
        _load(dir_path)
    run_rules(dir_path)


def _load(dir_path):
    main = _get_main_file()
    launchd.load(
        rule_name=os.path.splitext(os.path.split(main)[-1])[0],
        rule_path=os.path.abspath(main),
        path_to_observe=dir_path
    )


def _get_main_file():
    return sys.modules['__main__'].__file__


def run_rules(dir_path=None, paths=None, rules=None):
    rules = rules or Rule.__subclasses__()
    for path in _chain_paths(dir_path, paths):
        if isinstance(path, str):
            path = path.decode('utf-8')
        prev_path = path
        for rule in rules:
            r = rule(prev_path)
            r.do()
            prev_path = r.fullpath


def _chain_paths(dir_path, paths):
    dir_path = os.path.expanduser(dir_path) if dir_path else None
    paths_in_dir = (
        os.path.join(dir_path, fn) for fn in os.listdir(dir_path)
    ) if dir_path else iter(())
    paths = iter(paths) if paths else iter(())
    return chain(paths_in_dir, paths)


def logged(f):
    @wraps(f)
    def to_log(self, *args, **kwargs):
        msg = '{}: {} - {}'.format(
            f.__name__, _get_main_file(),
            ', '.join((unicode(a) for a in args))
        )
        try:
            f(self, *args, **kwargs)
            logger.success(msg)
        except Exception as e:
            logger.error(msg + ' ' + unicode(e))
    return to_log


class Whens(object):
    movie_extensions = (
        'mov', 'mp4', 'mkv', 'avi', 'wmv', 'flv', 'm4v', 'mpg'
    )
    image_extensions = (
        'jpg', 'jpeg', 'gif', 'svg', 'png'
    )
    book_extensions = (
        'pdf', 'epub', 'mobi'
    )
    comic_extensions = (
        'cbr', 'cbz'
    )
    text_extensions = (
        'txt', 'markdown', 'md', 'taskpaper'
    )

    def name_contains(self, word):
        return word in self.lower_name

    def name_contains_all(self, *args):
        return all((self.name_contains(word) for word in args))

    def name_contains_any(self, *args):
        return any((self.name_contains(word) for word in args))

    def extension_in(self, *args):
        return self.extension in args

    def is_movie(self):
        return self.extension_in(*self.movie_extensions)

    def is_book(self):
        return self.extension_in(*self.book_extensions)

    def is_image(self):
        return self.extension_in(*self.image_extensions)

    def is_comic(self):
        return self.extension_in(*self.comic_extensions)

    def is_text(self):
        return self.extension_in(*self.text_extensions)

    def is_dir(self):
        return os.path.isdir(self.fullpath)

    def has_tag(self, tag):
        return tags.has_tag(self.fullpath, tag)


class Thens(object):
    @logged
    def move(self, to_path):
        to_path = os.path.expanduser(to_path)
        self._make_dirs(to_path)
        full_to_path = self._gen_new_path(to_path)
        shutil.move(self.fullpath, full_to_path)
        print full_to_path
        self.set_path(full_to_path)

    def _make_dirs(self, path):
        try:
            os.makedirs(path)
        except OSError as e:
            if not e.errno == 17:
                raise

    def _gen_new_path(self, to_path):
        new_path = os.path.join(to_path, self.name + '.' + self.extension)
        file_index = 1
        while os.path.exists(new_path):
            new_path = os.path.join(
                to_path, self.name + unicode(file_index) + '.' + self.extension
            )
            file_index += 1
        return new_path

    @logged
    def tag(self, tag):
        tags.add_tag(self.fullpath, tag)

    @logged
    def open(self):
        subprocess.call(['open', self.fullpath])

    @logged
    def add_ctimestamp(self):
        cdate = self.get_cdate()
        self.rename(cdate.strftime('%F ') + self.name)

    @logged
    def trash(self):
        shutil.move(self.fullpath, os.path.expanduser('~/.Trash'))

    @logged
    def notify(self, msg, title='Valet'):
        subprocess.call([
            'osascript', '-e',
            'display notification "{msg}" with title "{title}"'.format(
                msg=msg, title=title
            ),
        ])

    @logged
    def rename(self, new_name):
        new_path = os.path.expanduser(
            os.path.join(self.dirpath, new_name + '.' + self.extension)
        )
        shutil.move(self.fullpath, new_path)
        self.set_path(new_path)

    def get_cdate(self):
        return dt.datetime.utcfromtimestamp(
            os.path.getctime(self.fullpath)
        )

    def read(self):
        with open(self.fullpath) as f:
            return f.read()

    def call(self, command):
        return subprocess.call(command)


class Rule(Whens, Thens):
    def __init__(self, path):
        self.set_path(path)

    def set_path(self, path):
        self.fullpath = os.path.expanduser(path)
        self.dirpath, self.filename = os.path.split(path)
        self.name, dot_extension = os.path.splitext(self.filename)
        self.lower_name = self.name.lower()
        self.extension = dot_extension.lstrip('.')

    def do(self):
        self.prepare()
        if self.when():
            self.then()
        self.finish()

    def when(self):
        return True

    def then(self):
        raise NotImplementedError()

    def prepare(self):
        pass

    def finish(self):
        pass
