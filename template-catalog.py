#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    template-catalog.py: VIVO Template Catalog

    VIVO and Vitro use Freemarker templates (a lot of them!) to create the user interface. It is difficult for anyone
    to know which templates do what and where things might be in the templates.

"""

# TODO: To count VIVO, process Vitro and then VIVO.  Add then templates

__author__ = "Michael Conlon"
__copyright__ = "Copyright (c) 2017 Michael Conlon"
__license__ = "Apache-2 license"
__version__ = "0.2.0"


def file_len(fname):
    """
    Determine the number of lines in a file
    :param fname:
    :return:
    """
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def file_count_i18n(fname):
    """
    Determine the number of lines in a file
    :param fname:
    :return:
    """
    with open(fname) as f:
        data = f.read()
        return data.count('${i18n().')


def file_tree(ftl, name, indent=0):
    """
    given the ftl structure and a name, print the file tree for the name.  For each name called,
    print the file tree (recursive)
    :param ftl:
    :param name:
    :return:
    """
    if ftl[name]['ncalls'] == 0:
        return
    indent += 4
    for nm in ftl[name]['calls']:
        print ' ' * indent, nm
        file_tree(ftl, nm, indent)


def file_calls(fname):
    """
    Determine the templates called by this template
    :param fname:
    :return:
    """
    calls = set()
    with open(fname) as f:
        skip = False
        for i, l in enumerate(f):
            if '<#--' in l:
                skip = True
            if '-->' in l:
                skip = False
                continue
            if skip:
                continue
            if '.ftl' in l:
                end = l.find('.ftl')
                search = l[0:end+4][::-1]
                start = search.find('"')
                name = search[0:start][::-1]
                if name not in calls:
                    calls.add(name)
    return calls


def file_has_text(fname):
    """
    Determine the templates called by this template
    :param fname:
    :return:
    """
    import re
    has_text = False
    with open(fname) as f:
        skip = False
        for i, l in enumerate(f):
            if '<#--' in l or '<!--' in l or '<script' in l:
                skip = True
            match = re.search(r'<#[a-z]', l)
            if match:
                continue
            if '<@' in l:
                continue
            if '-->' in l or '</script>' in l:
                skip = False
                continue
            if skip:
                continue

            match = re.search(r' [a-z]+ ', l)
            if match:
                has_text = True
                print fname, "text = ", l
                break
    return has_text


def main():
    """
    The main function.  Does the work
    :return: None
    """
    import os

    root_dir = '/Users/mikeconlon/PycharmProjects/Vitro/webapp/src'
    count = 0
    ftl = {}

    for directory, subdirectories, files in os.walk(root_dir):
        for file_name in files:
            if file_name.endswith('.ftl'):
                path_name = os.path.join(directory, file_name)
                calls = file_calls(path_name)
                count += 1
                ftl[file_name] = {}
                ftl[file_name]['lines'] = file_len(path_name)
                ftl[file_name]['path'] = path_name
                ftl[file_name]['ncalls'] = len(calls)
                ftl[file_name]['calls'] = calls
                ftl[file_name]['called'] = 0
                ftl[file_name]['has_text'] = file_has_text(path_name)
                ftl[file_name]['i18n'] = file_count_i18n(path_name)

    for file_name in ftl:
        for name in ftl[file_name]['calls']:
            ftl[name]['called'] += 1

    print "\n", count, "templates"
    for name in ftl:
        print name, 'has text = ', ftl[name]['has_text'], 'i18n count =', ftl[name]['i18n'], 'lines =', \
            ftl[name]['lines']
        file_tree(ftl, name)

if __name__ == "__main__":
    main()

