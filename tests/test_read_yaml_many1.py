#!/usr/bin/env python3
from unittest import TestCase
from collections import OrderedDict
from ebnflib.read_yaml.read import reads
from ebnflib.models import (
    EbnfMany1,
    EbnfMap,
    EbnfStr,
    EbnfToken)

TAG_HEADER = "%TAG ! tag:drosoft.org/ebnf,2016:\n---\n"


class ReadYamlScalars(TestCase):

    def test_always(self):
        self.assertTrue(True)

    def test_many1_rule(self):
        # discouraged, but allowed, should be !many1 [digit]
        t = reads(TAG_HEADER + "top: !many1 digit")
        self.assertTrue(isinstance(t, EbnfMap))
        self.assertTrue(isinstance(t.rules, OrderedDict))
        t2 = t.rules['top']
        print(repr(t2))
        self.assertTrue(isinstance(t2, EbnfMany1))
        self.assertTrue(isinstance(t2.many1, EbnfStr))
        self.assertTrue(t2.many1.rule == 'digit')

    def test_many1_empty_list(self):
        t = reads(TAG_HEADER + "top: !many1 []")
        self.assertTrue(isinstance(t, EbnfMap))
        self.assertTrue(isinstance(t.rules, OrderedDict))
        t2 = t.rules['top']
        self.assertTrue(isinstance(t2, EbnfMany1))
        self.assertTrue(isinstance(t2.many1, list))
        self.assertTrue(t2.many1 == [])

    def test_many1_rule_list_2(self):
        t = reads(TAG_HEADER + "top: !many1 ['lt', True]")
        self.assertTrue(isinstance(t, EbnfMap))
        self.assertTrue(isinstance(t.rules, OrderedDict))
        t2 = t.rules['top']
        self.assertTrue(isinstance(t2, EbnfMany1))
        self.assertTrue(isinstance(t2.many1, list))
        t3 = t2.many1
        self.assertTrue(len(t3) == 2)
        self.assertTrue(isinstance(t3[0], EbnfStr))
        self.assertTrue(t3[0].rule == 'lt')
        self.assertTrue(t3[1] == True)

    def test_many1_token_list_2(self):
        t = reads(TAG_HEADER + "top: !many1 [!token 'lt', True]")
        self.assertTrue(isinstance(t, EbnfMap))
        self.assertTrue(isinstance(t.rules, OrderedDict))
        t2 = t.rules['top']
        self.assertTrue(isinstance(t2, EbnfMany1))
        self.assertTrue(isinstance(t2.many1, list))
        t3 = t2.many1
        self.assertTrue(len(t3) == 2)
        self.assertTrue(isinstance(t3[0], EbnfToken))
        self.assertTrue(t3[0].token == 'lt')
        self.assertTrue(t3[1] == True)
