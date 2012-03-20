#!/usr/bin/env python

"""
Module to provide creation of a static HTML website
"""

import argparse
import os
import re
import shutil


HEADER_TEMPLATE = 'header.html'
FOOTER_TEMPLATE = 'footer.html'


# FIXME: Optimize opening templates only once


def _get_template_html(template):
    """Get html content from template"""

    try:
        handle = open(template, 'r')
        handle_html = handle.read()
    except IOError:
        # FIXME: Default this to at least an html doctype, etc.
        print 'Missing template %s, continuing without it' % (template)
        handle_html = ""

    return handle_html


def convertFile(src_file, dest_file, templates):
    """Convert src file into html and add in site layout, etc."""

    import markdown

    md = markdown.Markdown()

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

    dest_stream.write(_get_template_html(templates['header']))
    dest_stream.write('<h1>%s</h1>' % os.path.basename(dest_file).split(
                                                                os.extsep)[0])
    dest_stream.write(html)
    dest_stream.write(_get_template_html(templates['footer']) + '\n')


def _normalize_paths(src_dir, dest_dir, templates):
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

    # If relative path is given for template assume it's relative to src
    for template, filename in templates.iteritems():
        if not os.path.isabs(filename):
            templates[template] = os.path.join(src_dir, filename)

    return (src_dir, dest_dir, templates)


def generate(src_dir, dest_dir, templates):
    """Generate html from markdown files in src_dir and place in dest_dir"""

    if not os.path.isdir(src_dir):
        print "Source directory (%s) doesn't exist" % (src_dir)
        return 0

    src_dir, dest_dir, templates = _normalize_paths(src_dir, dest_dir,
                                                                    templates)

    for root, dirs, files in os.walk(src_dir):
        for file_name in files:
            # dest file will be same name/location with just dest_dir swapped
            # out for src_dir
            src_file = os.path.join(root, file_name)
            dest_file = re.sub(src_dir, dest_dir, src_file)

            markdown = file_name.endswith(''.join([os.extsep, 'md']))
            if markdown:
                # Write to the same filename just swap .md for .html
                dest_file = ''.join([dest_file.split(os.extsep)[0], os.extsep,
                                    'html'])

            try:
                os.makedirs(os.path.dirname(dest_file))
            except OSError:
                # Already exists
                pass

            if markdown:
                convertFile(src_file, dest_file, templates)
            else:
                shutil.copyfile(src_file, dest_file)


def main():
    """main"""

    parser = argparse.ArgumentParser(description='Static website generator',
                   formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('content_dir', type=str,
                        help='Path to main directory of markdown content')

    parser.add_argument('-header', type=str, default=HEADER_TEMPLATE,
                        help='name of HTML file to use as header template')

    parser.add_argument('-footer', type=str, default=FOOTER_TEMPLATE,
                        help='name of HTML file to use as footer template')

    args = parser.parse_args()

    templates = {'header': args.header, 'footer': args.footer}

    # Get all markdown files organized by subdirectory
    generate(args.content_dir, '_static', templates)


if __name__ == "__main__":
    main()
