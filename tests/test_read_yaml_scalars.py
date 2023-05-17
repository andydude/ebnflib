#!/usr/bin/env python3
from unittest import TestCase
from collections import OrderedDict
from ebnflib.read_yaml.read import reads
from ebnflib.models import (
    EbnfEmpty,
    EbnfMap)

TAG_HEADER = "%TAG ! tag:drosoft.org/ebnf,2016:\n---\n"


class ReadYamlScalars(TestCase):

    def test_always(self):
        self.assertTrue(True)

    def test_empty_null(self):
        t = reads(TAG_HEADER + "top: !empty null")
        self.assertTrue(isinstance(t, EbnfMap))
        self.assertTrue(isinstance(t.rules, OrderedDict))
        t2 = t.rules['top']
        self.assertTrue(isinstance(t2, EbnfEmpty))
        self.assertTrue(t2.empty == 'null') 	# strict str option
        # self.assertTrue(t2.empty == None) 	# passthrough option

    def test_empty_bool_true(self):
        t = reads(TAG_HEADER + "top: !empty true")
        self.assertTrue(isinstance(t, EbnfMap))
        self.assertTrue(isinstance(t.rules, OrderedDict))
        t2 = t.rules['top']
        self.assertTrue(isinstance(t2, EbnfEmpty))
        self.assertTrue(t2.empty == 'true') 	# strict str option
        # self.assertTrue(t2.empty == True) 	# passthrough option

    def test_empty_bool_false(self):
        t = reads(TAG_HEADER + "top: !empty false")
        self.assertTrue(isinstance(t, EbnfMap))
        self.assertTrue(isinstance(t.rules, OrderedDict))
        t2 = t.rules['top']
        self.assertTrue(isinstance(t2, EbnfEmpty))
        self.assertTrue(t2.empty == 'false') 	# strict str option
        # self.assertTrue(t2.empty == False) 	# passthrough option

    def test_empty_empty_str(self):
        t = reads(TAG_HEADER + "top: !empty ''")
        self.assertTrue(isinstance(t, EbnfMap))
        self.assertTrue(isinstance(t.rules, OrderedDict))
        t2 = t.rules['top']
        self.assertTrue(isinstance(t2, EbnfEmpty))
        self.assertTrue(isinstance(t2.empty, str))
        self.assertTrue(t2.empty == '')

    def test_empty_comment(self):
        t = reads(TAG_HEADER + "top: !empty 'hello'")
        self.assertTrue(isinstance(t, EbnfMap))
        self.assertTrue(isinstance(t.rules, OrderedDict))
        t2 = t.rules['top']
        self.assertTrue(isinstance(t2, EbnfEmpty))
        self.assertTrue(isinstance(t2.empty, str))
        self.assertTrue(t2.empty == 'hello')
