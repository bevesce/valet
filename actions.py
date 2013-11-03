import subprocess
import shutil
import os
import valet

### Helpers ###

def _add_number_to_filename(src):
    splitted = src.split('.')
    if len(splitted) == 1:
        return src + '1'
    prefix = '.'.join(splitted[0:-1])
    postfix = splitted[-1]
    if prefix[-1].isdigit():
        prefix = prefix[0:-1] + str(int(prefix[-1]) + 1)
    else:
        prefix += '1'
    return prefix + '.' + postfix


### Actions ###

def move(path, path_to):
    valet.log('[+] moving {0} to {1}'.format(path, path_to))
    try:
        if not os.path.exists(path_to):
            os.makedirs(path_to)
        shutil.move(path, path_to)
        valet.log('[+] moved')    
    except shutil.Error as e:
        if str(e)[-14:] == 'already exists':
            newsrc = _add_number_to_filename(path)
            os.rename(path, newsrc)
            move(newsrc, path_to)
            return newsrc
        else:
            pass
    except (IOError, OSError):
        pass


def tag(path, tags):
    if isinstance(tags, str):
        tags = [tags]
    for tag_str in tags:
        valet.log('[+] tagging {0} with {1}'.format(path, tag_str))
        subprocess.check_output('/usr/local/bin/tag -a {0} "{1}"'.format(tag_str, path), shell=True)
    valet.log('[+] tagged' )