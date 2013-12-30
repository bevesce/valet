import sys
import os
import subprocess

launchd_deamon_plist_template = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>Label</key>
	<string>com.valet.{rule_name}</string>
	<key>ProgramArguments</key>
	<array>
		<string>/usr/bin/python</string>
		<string>{rule_path}</string>
	</array>
	<key>RunAtLoad</key>
	<true/>
	<key>WatchPaths</key>
	<array>
		<string>{path_to_observe}</string>
	</array>
</dict>
</plist>
"""


if len(sys.argv) != 4:
	print 'rule_name rule_path path_to_observe'
	sys.exit(0)

rule_name = sys.argv[1]
rule_path = sys.argv[2]
path_to_observe = sys.argv[3]

rule_path = os.path.abspath(rule_path)
path_to_observe = os.path.abspath(path_to_observe)

launchd_deamon_plist = launchd_deamon_plist_template.format(
	rule_name=rule_name,
	rule_path=rule_path,
	path_to_observe=path_to_observe
)

deamons_path = '/Users/bvsc/Library/LaunchAgents/com.valet.' + rule_name + '.plist'
with open(deamons_path, 'w') as f:
	f.write(launchd_deamon_plist)
subprocess.call('launchctl load ' + deamons_path + '', shell=True)

