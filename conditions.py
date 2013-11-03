import os

movie_extensions = ['mov', 'mp4', 'mkv', 'avi', 'wmv', 'flv']
image_extensions = ['jpg', 'jpeg', 'gif', 'svg', 'png']
book_extensions = ['pdf', 'epub', 'mobi', 'cbr', 'cbz']


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