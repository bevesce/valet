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
    <false/>
    <key>WatchPaths</key>
    <array>
        <string>{path_to_observe}</string>
    </array>
</dict>
</plist>
"""


def load(rule_name, rule_path, path_to_observe):
    rule_path = os.path.abspath(rule_path)
    launchd_deamon_plist = launchd_deamon_plist_template.format(
        rule_name=rule_name,
        rule_path=rule_path,
        path_to_observe=os.path.expanduser(path_to_observe)
    )
    deamons_path = os.path.expanduser(''.join([
        '~/Library/LaunchAgents/com.valet.', rule_name, '.plist'
    ]))
    with open(deamons_path, 'w') as f:
        f.write(launchd_deamon_plist)
    subprocess.call('launchctl load ' + deamons_path + '', shell=True)
    print('Loaded {}: {} on {}'.format(
        rule_name, rule_path, path_to_observe
    ))
