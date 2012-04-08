#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import shutil

import markdown
import lib.templite
md = markdown.Markdown(extensions=['codehilite'])


def publish_markdown(source, target):
    inf = open(source)
    content = md.convert(inf.read())
    inf.close()
    outf = open(target, 'w')
    outf.write(wrap_template(content))
    outf.close()

def passthru(source, target):
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

def wrap_template(content):
    return T.render(dict(content=content))


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
    parser(sourcename, targetname)
    
def push_resources(res, target):
    for name in os.listdir(res):
        if name != TEMPLATE:
            shutil.copy(res+"/"+name, target)
        