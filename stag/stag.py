#!/usr/bin/env python

"""
Module to provide creation of a static HTML website
"""

import argparse
import markdown
import os
import re


HEADER_TEMPLATE = 'layout/header.html'


def convertFile(src_file, dest_file, header_template):
    """Convert src file into html and add in site layout, etc."""

    md = markdown.Markdown()

    try:
        header = open(header_template, 'r')
        header_html = header.read()
    except IOError:
        # FIXME: Default this to at least an html doctype, etc.
        print 'Missing header template, continuing without it'
        header_html = ""

    try:
        html = md.convert(open(src_file).read())
    except IOError:
        print 'Unable to read src file: %s, skipping' % (src_file)
        return

    try:
        dest_stream = open(dest_file, 'w')
    except IOError:
        print 'Unable to write destination file %s, skipping' % (dest_file)
        return

    dest_stream.write(header_html)
    dest_stream.write('<h1>%s</h1>' % dest_file.split(os.extsep)[0])
    dest_stream.write(html + "\n")

    # Open header file
    # Convert src to stream md.convert(open(src_file).read())
    # Write header html to dest_file
    # Write title, h1 (filename) to dest_file
    # Write converted source to dest_file
    # Open footer file
    # Write footer to file


def _normalize_paths(src_dir, dest_dir, header_template):
    """Normalize all pathing for arguments
        - Need trailing slashes
        - Need all dirs to be either absolute or relative paths
        - Templates need directory name
    """

    # Make sure both paths are either absolute or relative
    if os.path.isabs(src_dir):
        dest_dir = os.path.abspath(dest_dir)
    else:
        dest_dir = os.path.relpath(dest_dir)

    # Make sure we have a trailing slashes
    dest_dir = os.path.normpath(dest_dir) + os.sep
    src_dir = os.path.normpath(src_dir) + os.sep

    # If relative path is given for header template assume it's relative to the
    # src directory
    if not os.path.isabs(header_template):
        header_template = os.path.join(src_dir, header_template)

    return (src_dir, dest_dir, header_template)


def generate(src_dir, dest_dir, header_template):
    """Generate html from markdown files in src_dir and place in dest_dir"""

    if not os.path.isdir(src_dir):
        print "Source directory (%s) doesn't exist" % (src_dir)
        return 0

    src_dir, dest_dir, header_template = _normalize_paths(src_dir, dest_dir,
                                                          header_template)

    for root, dirs, files in os.walk(src_dir):
        for file_name in files:
            if not file_name.endswith(''.join([os.extsep, 'md'])):
                continue

            # dest file will be same name/location with just dest_dir swapped
            # out for src_dir
            src_file = os.path.join(root, file_name)
            dest_file = re.sub(src_dir, dest_dir, src_file)

            # Write to the same filename just swap .md for .html
            dest_file = ''.join([dest_file.split(os.extsep)[0], os.extsep,
                                'html'])
            try:
                os.makedirs(os.path.dirname(dest_file))
            except OSError:
                # Already exists
                pass

            convertFile(src_file, dest_file, header_template)


def main():
    """main"""

    parser = argparse.ArgumentParser(description='Static website generator',
                   formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('content_dir', type=str,
                        help='Path to main directory of markdown content')

    parser.add_argument('-header_template', type=str,
                        default=HEADER_TEMPLATE,
                        help='HTML file to use as header template')

    args = parser.parse_args()

    # Get all markdown files organized by subdirectory
    generate(args.content_dir, '_static', args.header_template)


if __name__ == "__main__":
    main()
