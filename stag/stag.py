#!/usr/bin/env python

"""
Module to provide creation of a static HTML website
"""

import os
import argparse


def get_markdown_files(content_dir, md_files):
    """Get a list of all the markdown files in given directory"""

    for root, dirs, files in os.walk(content_dir):
        for dir_name in dirs:
            if dir_name.startswith('.'):
                continue

            md_files[dir_name] = []
            rel_path = os.path.join(root, dir_name)
            get_markdown_files(rel_path, md_files)

        for file_name in files:
            if file_name.startswith('.'):
                continue

            if file_name.endswith('.md'):
                dir_name = os.path.basename(content_dir)

                try:
                    md_files[dir_name].append(file_name)
                # Directory with no subdirectories
                except KeyError:
                    md_files[dir_name] = []
                    md_files[dir_name].append(file_name)

        return md_files


def main(content_dir):
    """main"""


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Static website generator')
    parser.add_argument('content_dir', type=str,
                        help='Full path to main directory of markdown content')
    args = parser.parse_args()

    print get_markdown_files(args.content_dir, {})
