#!/usr/bin/env python

"""
Module to provide creation of a static HTML website
"""

import os
import argparse
import markdown


def generate(src_dir, dest_dir):
    """"""

    md = markdown.Markdown()

    # Make sure directory has os dependent trailing slash
    src_dir = os.path.normpath(src_dir) + os.sep
    dest_dir = os.path.normpath(dest_dir) + os.sep

    for root, dirs, files in os.walk(src_dir):
        gen_dir = os.path.join(dest_dir, os.path.basename(root))

        try:
            os.makedirs(gen_dir)
        except OSError:
            # Already exists
            pass

        for file_name in files:
            if not file_name.endswith(''.join([os.extsep, 'md'])):
                continue

            # We're going to write to the same filename just swap .md for .html
            dest_file = ''.join([file_name.split(os.extsep)[0], os.extsep,
                                'html'])
            md.convertFile(os.path.join(root, file_name),
                           os.path.join(gen_dir, dest_file))


def main(content_dir):
    """main"""

    # Get all markdown files organized by subdirectory
    generate(args.content_dir, '_static')
    #print get_markdown_files(args.content_dir, {})

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Static website generator')
    parser.add_argument('content_dir', type=str,
                        help='Full path to main directory of markdown content')
    args = parser.parse_args()

    main(args.content_dir)
