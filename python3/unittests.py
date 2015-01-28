#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Unit testing testing...
"""

import unittest
import datetime
import analyze_gmail

class TestAnalyzeGmail(unittest.TestCase):

    def setUp(self):
        pass

    def test_tv_job_constructor(self):
        pass

    def test_parse_quoted_email_string(self):
        inp_str = '"Active.com Email Exclusive" <active_offers@news1-active.com>k.com>'
        output = analyze_gmail.parse_quoted_email_string(inp_str)
        self.assertEqual(output[0], 'active_offers@news1-active.com')

if __name__ == '__main__':
    unittest.main()
