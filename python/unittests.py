#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Unit testing testing...
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import unittest
import datetime
import analyze_gmail


class TestAnalyzeGmail(unittest.TestCase):

    def setUp(self):
        pass

    def test_parse_quoted_email_string(self):
        inp_str = '"Active.com Email Exclusive" <active_offers@news1-active.com>k.com>'
        output = analyze_gmail.parse_quoted_email_string(inp_str)
        self.assertEqual(output[0], 'active_offers@news1-active.com')


if __name__ == '__main__':
    unittest.main()
