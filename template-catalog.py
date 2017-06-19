#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    template-catalog.py: VIVO Template Catalog

    VIVO and Vitro use Freemarker templates (a lot of them!) to create the user interface. It is difficult for anyone
    to know which templates do what and where things might be in the templates.

    Usage:

    template-catalog [theme]

    If theme starts with a v it is assumed to be a vitro theme and the "v" is removed.

    For vitro themes, the vitro templates are processed, then the vitro theme templates

    For VIVO themes, the vitro templates are processed, then the VIVO templates, then the vivo theme templates

    The default theme is wilma

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


def process_path(ftl, path):
    """
    Given a path, process all the directories and files in the path looking for Freemarker templates.
    For each template, compute templates stats
    :param path:
    :return: None
    """
    import os

    for directory, subdirectories, files in os.walk(path):
        for file_name in files:
            if file_name.endswith('.ftl'):
                path_name = os.path.join(directory, file_name)
                calls = file_calls(path_name)
                ftl[file_name] = {}
                ftl[file_name]['lines'] = file_len(path_name)
                ftl[file_name]['path'] = path_name
                ftl[file_name]['ncalls'] = len(calls)
                ftl[file_name]['calls'] = calls
                ftl[file_name]['called'] = 0
                ftl[file_name]['has_text'] = file_has_text(path_name)
                ftl[file_name]['i18n'] = file_count_i18n(path_name)


def main():
    """
    The main function.  Does the work
    :return: None
    """

    import sys

    ftl = {}  # structure to contain template info, keyed by template file_name

    if len(sys.argv) == 1:
        theme = "vvitro"
    else:
        theme = sys.argv[1]

    root_dir = '/Users/mikeconlon/PycharmProjects/'
    vitro_dir = 'Vitro/webapp/src'
    vivo_dir = 'VIVO/webapp/src'

    if theme[0] == 'v':
        theme_dir = 'Vitro/webapp/src/main/webapp/themes/' + theme[1:]
        process_path(ftl, root_dir+vitro_dir)
        process_path(ftl, root_dir+theme_dir)
    else:
        theme_dir = 'VIVO/webapp/src/main/webapp/themes/' + theme
        process_path(ftl, root_dir+vitro_dir)
        process_path(ftl, root_dir+vivo_dir)
        process_path(ftl, root_dir+theme_dir)

    for file_name in ftl:
        for name in ftl[file_name]['calls']:
            ftl[name]['called'] += 1

    print "\n", len(ftl), "templates for theme", theme
    for name in ftl:
        print name, 'has text = ', ftl[name]['has_text'], 'i18n count =', ftl[name]['i18n'], 'lines =', \
            ftl[name]['lines']
        file_tree(ftl, name)

if __name__ == "__main__":
    main()

