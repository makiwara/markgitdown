#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys;reload(sys);sys.setdefaultencoding('utf-8'); import os, optparse
from pprint import pprint

import prepare
import git

# Option parser
parser = optparse.OptionParser(description='Markdown files to html from git. Run and get on with your life.')
parser.add_option('-s', dest='source', default='./source', help='Documentation source', metavar='SOURCE')
parser.add_option('-t', dest='target', default='./build', help='Documentation output target', metavar='TARGET')
parser.add_option('-r', dest='resources', default='./resource', help='Template and resources', metavar='RESOURCES')
parser.add_option('-f', dest='force', action="store_true", default=False, help='Force rebuild', metavar='FORCE')

(options, args) = parser.parse_args()

# check git & update only if needed
need_refresh = git.pull(options.source)
if options.force or need_refresh:
    # reset state
    prepare.empty_target(options.target)
    prepare.init_template(options.resources)
    # publish all
    items = prepare.get_items(options.source)
    for item in items:
        targetdir = options.target + item[0][len(options.source):]
        prepare.ensure_dir(targetdir)
        prepare.push_resources(options.resources, targetdir)
        for name in item[2]:
            prepare.push_file(item[0], targetdir, name)




