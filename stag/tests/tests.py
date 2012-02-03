"""
Simple unit tests for stag package
"""

import os
import re
import shutil
import unittest

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

        stag.generate(self.src_dir, self.dest_dir)

        self.assertTrue(os.path.isdir(self.dest_dir),
                                                'Missing %s' % (self.dest_dir))

        for root, dirs, files in os.walk(self.src_dir):
            for file_name in files:
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
        self.generateAndCheck()

    def test_generate_rel_path(self):
        """
        Verify all .md files in src path are in identical place as a .html file
        in relative dest path
        """

        self.src_dir = 'stag/tests/_test_site'
        self.dest_dir = 'stag/tests/_gen_site'
        self.generateAndCheck()

    def test_missing_src_dir(self):
        """Verify missing src directory is handled"""

        self.src_dir = 'this/is/not/a/real/dir'
        self.dest_dir = 'dest'
        self.assertTrue(stag.generate(self.src_dir, self.dest_dir) == 0)

    def tearDown(self):
        """teardown"""

        if os.path.isdir(self.dest_dir):
            shutil.rmtree(self.dest_dir)
