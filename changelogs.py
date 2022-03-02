#!/usr/bin/env python3

template = '''Added:
  Feature A:
  - abcdef Added something
Changed:
  Change B:
  - bcdefa Removed something
Fixed:
  Bugfix C:
  - cdefab Fixed something
Unclassified:
  Unclassified commits:
'''

import argh

date_format = '%Y-%m-%d,%H:%M:%S'

# it should eventually be possible to just supply a list of repos
@argh.arg('gitlogs', nargs='+', help='list of giltog files')
def parse_gitlogs(gitlogs):
    "Takes in n files as input, spits out a template changelog YAML."
    changelog_yaml = template
    commits = []
    for gitlog in gitlogs:
        with open(gitlog, 'r') as gl:
            commit_lines = gl.readlines()
            for c in commit_lines:
                ref, datestr, msg = c.split(' | ')
                commit = {'ref': ref, 'date': datestr, 'msg': msg.strip()}
                commits += [commit]

    from datetime import datetime
    commits.sort(key=lambda c: datetime.strptime(c['date'], date_format))

    for c in commits:
        changelog_yaml += f"  - {c['ref']} {c['msg']}\n"
    print(changelog_yaml)

import yaml

def print_changelog(filename):
    "Takes in a YAML file with ordered changelog, spits out human-readable changelog."
    with open(filename, "r") as stream:
        try:
            data = yaml.safe_load(stream)
            for section in data:
                # skip sections with no features in them
                if data[section] is not None:
                    print(f'{section}:')
                    for feature in data[section]:
                        print(f'* {feature}')
                        if feature == 'Unclassified commits':
                            commits_left = 0
                            if data[section][feature] is not None:
                                commits_left = len(data[section][feature])
                            print(f'{commits_left} commits left.')
        except yaml.YAMLError as exc:
            print(exc)

parser = argh.ArghParser()
parser.add_commands([parse_gitlogs, print_changelog])

if __name__ == '__main__':
    parser.dispatch()
