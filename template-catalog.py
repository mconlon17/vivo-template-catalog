#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    template-catalog.py: VIVO Template Catalog

    VIVO and Vitro use Freemarker templates (a lot of them!) to create the user interface. It is difficult for anyone
    to know which templates do what and where things might be in the templates.

"""

# TODO: improve handling of comments in the templates
# TODO: Add code for recursive tree of calls for each template
# TODO: Add counts for calls for each template

__author__ = "Michael Conlon"
__copyright__ = "Copyright (c) 2017 Michael Conlon"
__license__ = "Apache-2 license"
__version__ = "0.0.1"


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


def file_calls(fname):
    """
    Determine the templates called by this template
    :param fname:
    :return:
    """
    calls = set()
    with open(fname) as f:
        for i, l in enumerate(f):
            if '<#--' in l:
                continue
            if '.ftl' in l:
                end = l.find('.ftl')
                search = l[0:end+4][::-1]
                start = search.find('"')
                name = search[0:start][::-1]
                if name not in calls:
                    calls.add(name)
    return calls


def main():
    """
    The main function.  Does the work
    :return: None
    """
    import os

    root_dir = '/Users/mikeconlon/PycharmProjects/VIVO/webapp/src'
    count = 0

    for directory, subdirectories, files in os.walk(root_dir):
        for file_name in files:
            if file_name.endswith('.ftl'):
                path_name = os.path.join(directory, file_name)
                print file_len(path_name), file_name, file_calls(path_name)
                count += 1

    print "\n", count, "templates"


if __name__ == "__main__":
    main()

