import sys
import os
import actions, conditions

_rules = []

def rule(fun):
    _rules.append(fun)
    return fun


def run_rules(path, rules):
	if not path:
		return
	if path[-1] != '/':
		path += '/'	
	path = os.path.expanduser(path)
	for filename in os.listdir(path):
		if filename[0] == '.':
			continue
		for fun in rules:
			# log('[i] tries {0} on {1}'.format(fun.__name__, path + filename))
			fun(path + filename)


def run(path=None):
	if not path:
		path = ' '.join(sys.argv[1:])
	run_rules(path, _rules)


def log(txt):
	from datetime import datetime
	# print txt
	with open('/Users/bvsc/Desktop/valet_log.txt', 'a') as f:
		f.write(str(datetime.now()) + ' ' + txt + '\n')
