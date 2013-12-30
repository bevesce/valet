import os
from Foundation import NSPropertyListSerialization
from xattr import setxattr, getxattr

### Helpers ###

movie_extensions = ['mov', 'mp4', 'mkv', 'avi', 'wmv', 'flv', 'm4v', 'mpg']
image_extensions = ['jpg', 'jpeg', 'gif', 'svg', 'png']
book_extensions = ['pdf', 'epub', 'mobi', 'cbr', 'cbz']

 
def _get_item_where_froms(path):
    """Get kMDItemWhereFroms from a file, returns an array of strings or None if no value is set."""
    kMDItemWhereFroms = "com.apple.metadata:kMDItemWhereFroms"
    try:
        plist = buffer(getxattr(path, kMDItemWhereFroms))
        if plist:
            data = NSPropertyListSerialization.propertyListWithData_options_format_error_(plist, 0, None, None)[0]
            return data
    except KeyError:
        pass
    return None


### Conditions ###

"""
convention: if path is an argument it always should be first one
"""


def name_contains(path, word):
    return word in path.split('/')[-1]


def name_contains_all(path, words):
    for word in words:
        if not name_contains(path, word):
            return False
    return True


def name_contains_any(path, words):
    for word in words:
        if name_contains(path, word):
            return True
    return False


def extension_in(path, extensions):
	_, extension = os.path.splitext(path)
	extension = extension[1:]
	return extension.lower() in [ex.lower() for ex in extensions]


def extension_is(path, extension):
	_, file_extension = os.path.splitext(path)
	return file_extension.lower() == extension.lower()


def is_dir(path):
    return os.path.isdir(path)


def dir_contains_extensions(path, extensions):
    if not os.path.isdir(path):
        return False
    for filename in os.listdir(path):
        if extension_in(filename, extensions):
            return True
    return False


def any_where_froms_starts_with(path, start):
        where_froms = _get_item_where_froms(path)
        if not where_froms:
            return False
        for where_from in where_froms:
            if where_from.startswith(start):
                return True
        return False


def any_where_froms_constains(path, word):
        where_froms = _get_item_where_froms(path)
        if not where_froms:
            return False
        for where_from in where_froms:
            if word in where_from:
                return True
        return False

