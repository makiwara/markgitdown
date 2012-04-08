#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import shutil

import markdown
import lib.templite
md = markdown.Markdown(extensions=['codehilite'])


def publish_markdown(source, target, name):
    inf = open(source)
    source_content = inf.read()
    inf.close()
    content = md.convert(source_content)
    title = find_title(source_content)
    if not title: title = name
    outf = open(target, 'w')
    outf.write(wrap_template(content, title))
    outf.close()

def passthru(source, target, *a, **b):
    shutil.copy(source, target) 

DEFAULT = passthru
EXTENSIONS = dict(
    md= publish_markdown,
    mdown= publish_markdown,
    markdown= publish_markdown,
    )
TEMPLATE = 'page.html'


def init_template(resource):
    global T
    inf = open(resource+"/"+TEMPLATE)
    T = lib.templite.Templite(inf.read(), start="{{", end="}}")

def wrap_template(content, title):
    return T.render(dict(content=content, title=title))


def empty_target(target):
    if os.path.isdir(target):
        shutil.rmtree(target)

def ensure_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path)
    
def get_items(source):
    items = os.walk(source)
    return items
    
def push_file(source, target, name):
    sourcename = source + "/" + name
    targetname = target + "/" + name

    name, ext = os.path.splitext(sourcename)
    try:
        parser = EXTENSIONS[ext[1:]]
    except KeyError:
        parser = DEFAULT
    parser(sourcename, targetname, name)
    
def push_resources(res, target):
    for name in os.listdir(res):
        if name != TEMPLATE:
            shutil.copy(res+"/"+name, target)
            
def find_title(content):
    lines = content.splitlines()
    if len(lines) == 0:
        return None
    first_line = lines[0].strip()
    if first_line.startswith('#'):
        return first_line.lstrip('#')
    if len(lines) == 1:
        return None
    second_line = lines[1].strip()
    if second_line and (all(c == '=' for c in second_line) or (all(c == '-' for c in second_line))):
        return first_line
    return None    
        