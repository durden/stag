"""
Simple unit tests for stag package
"""

import os
import re
import shutil
import unittest

import markdown

import stag


class GenerateTests(unittest.TestCase):
    """Tests for the generate() method"""

    def setUp(self):
        """setup"""
        pass

    def generateAndCheck(self):
        """Generate site and verify all files exist"""

        self.assertTrue(os.path.isdir(self.src_dir),
                                                'Missing %s' % (self.src_dir))

        stag.generate(self.src_dir, self.dest_dir, self.header_template)

        self.assertTrue(os.path.isdir(self.dest_dir),
                                                'Missing %s' % (self.dest_dir))

        for root, dirs, files in os.walk(self.src_dir):
            for file_name in files:
                if not file_name.endswith(''.join([os.extsep, 'md'])):
                    continue

                gen_file = re.sub(self.src_dir, self.dest_dir,
                                                os.path.join(root, file_name))
                gen_file = os.path.normpath(re.sub('.md', '.html', gen_file))

                self.assertTrue(os.path.isfile(gen_file),
                                                    'Missing %s' % gen_file)

        for root, dirs, files in os.walk(self.dest_dir):
            for gen_file in files:
                self.assertTrue(gen_file.endswith('.html'),
                                                    'Non-html file in output')

    def test_generate_abs_path(self):
        """
        Verify all .md files in src path are in identical place as a .html file
        in absolute dest path
        """

        install_dir = os.path.dirname(stag.__file__)
        self.src_dir = os.path.join(install_dir, 'tests', '_test_site')
        self.dest_dir = os.path.join(install_dir, 'tests', '_gen_site')
        self.header_template = 'layout/header.html'
        self.generateAndCheck()

    def test_generate_rel_path(self):
        """
        Verify all .md files in src path are in identical place as a .html file
        in relative dest path
        """

        self.src_dir = 'stag/tests/_test_site'
        self.dest_dir = 'stag/tests/_gen_site'
        self.header_template = 'layout/header.html'
        self.generateAndCheck()

    def test_missing_src_dir(self):
        """Verify missing src directory is handled"""

        self.src_dir = 'this/is/not/a/real/dir'
        self.dest_dir = 'dest'
        self.header_template = 'layout/header.html'
        self.assertTrue(stag.generate(self.src_dir, self.dest_dir,
                                                    self.header_template) == 0)

    def tearDown(self):
        """teardown"""

        if os.path.isdir(self.dest_dir):
            shutil.rmtree(self.dest_dir)


class ConvertFileTests(unittest.TestCase):
    """Tests for the convertFile() method"""

    def setUp(self):
        """setup"""
        pass

    def test_convert_file(self):
        """Verify converting a file adds in header template and correct text"""

        md = markdown.Markdown()

        self.src_file = 'stag/tests/_test_site/about.md'
        self.dest_file = 'about.html'
        self.header_file = 'header.html'

        header = open(self.header_file, 'w')
        header_contents = '<html><head><title>Title</title></head><body>'
        header.write(header_contents)
        header.close()

        header_text = '<h1>%s</h1>' % (self.dest_file.split('.')[0])
        src_file_handle = open(self.src_file, 'r')
        correct_content = ''.join([header_contents, header_text,
                                        md.convert(src_file_handle.read()),
                                        '\n'])
        src_file_handle.close()

        stag.convertFile(self.src_file, self.dest_file, self.header_file)

        dest_file_handle = open(self.dest_file, 'r')
        gen_content = dest_file_handle.read()
        dest_file_handle.close()

        self.assertTrue(gen_content == correct_content,
                    'Generated content: \n%s\n\n Correct content:\n%s\n' % (
                        gen_content, correct_content))

    def tearDown(self):
        """teardown"""

        if os.path.isfile(self.dest_file):
            os.remove(self.dest_file)

        if os.path.isfile(self.header_file):
            os.remove(self.header_file)
