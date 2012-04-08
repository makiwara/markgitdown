#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import shutil
import re

from pprint import pprint

import markdown
import lib.templite
md = markdown.Markdown(extensions=['codehilite'])


def publish_markdown(source, target, name):
    inf = open(source)
    source_content = inf.read()
    inf.close()
    title = find_title(source_content)
    if not title: title = name
    toc, content = find_toc(source_content)
    content = md.convert(content)
    content = strip_toc(content)
    outf = open(target, 'w')
    outf.write(wrap_template(content, title, toc))
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

def wrap_template(content, title, toc):
    return T.render(dict(content=content, title=title, toc=toc))


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

def find_toc(content):
    lines = content.splitlines()
    pos = 0
    toc = []
    for line in lines:
        sline = line.strip()
        if pos > 0 and sline and all(c == '-' for c in sline) and lines[pos-1].strip():
           toc.append([pos-1, lines[pos-1].strip()]) 
        pos+=1
    for tocline in toc:
        lines[tocline[0]] = str(tocline[0])+'@@@@@@@@@@' + tocline[1]
    return toc, "\n".join(lines);
    
def strip_toc(html):
    return re.sub(r'([0-9]+)@@@@@@@@@@', r'<a class="anchor" href="#go\1" name="go\1">@</a>', html)

        