#!/usr/bin/python
# -*- coding: utf-8 -*-



from subprocess import Popen, PIPE


def _call(params, cwd=None):
    p =  Popen(params, stdout=PIPE, stderr=PIPE, cwd=cwd)
    output, error = p.communicate()
    # print output.strip()
    # print error.strip()
    # print p.returncode
    return output.strip(), error.strip(), p.returncode
    
    
    # fatal: '../waka-source' does not appear to be a git repository
    # fatal: The remote end hung up unexpectedly
    # 1
    
    # Already up-to-date.
    # 
    # 0
    
    # Updating ac2375b..b5bb9bf
    # ...
    # 0
    
    

def pull(path):
    output, error, code = _call(['git', 'pull'], cwd=path)
    if code != 0: return False
    if output == "Already up-to-date.": return False
    return True
