import subprocess

tag_base = '/usr/local/bin/tag '
default_tag_char = '#'


def add_tag(p, tag):
    subprocess.call(tag_base + '-a ' + tag + ' "' + p + '"', shell=True)


def add_tags(p, tags):
    subprocess.call(
        tag_base + '-a "' + ', '.join(tags) + '" "' + p + '"', shell=True
    )


def remove_tag(p, tag):
    subprocess.call(tag_base + '-r ' + tag + ' "' + p + '"', shell=True)


def remove_tags(p, tags):
    subprocess.call(
        tag_base + '-r "' + ', '.join(tags) + '" "' + p + '"', shell=True
    )


def list_tags(p):
    tags_raw = (
        subprocess.check_output(tag_base + '-l "' + p + '"', shell=True)
    ).decode('utf-8').strip()
    tags = tags_raw.replace(p, '').strip().split(',')
    return tags


def remove_all_tags(p):
    remove_tags(p, list_tags(p))


def has_tag(p, tag):
    return tag in list_tags(p)
