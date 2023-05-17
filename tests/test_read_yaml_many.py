#!/usr/bin/env python3
from unittest import TestCase
from collections import OrderedDict
from ebnflib.read_yaml.read import reads
from ebnflib.models import (
    EbnfMany,
    EbnfMap,
    EbnfStr,
    EbnfToken)

TAG_HEADER = "%TAG ! tag:drosoft.org/ebnf,2016:\n---\n"


class ReadYamlScalars(TestCase):

    def test_always(self):
        self.assertTrue(True)

    def test_many_rule(self):
        # discouraged, but allowed, should be !many [digit]
        t = reads(TAG_HEADER + "top: !many digit")
        self.assertTrue(isinstance(t, EbnfMap))
        self.assertTrue(isinstance(t.rules, OrderedDict))
        t2 = t.rules['top']
        print(repr(t2))
        self.assertTrue(isinstance(t2, EbnfMany))
        self.assertTrue(isinstance(t2.many, EbnfStr))
        self.assertTrue(t2.many.rule == 'digit')

    def test_many_empty_list(self):
        t = reads(TAG_HEADER + "top: !many []")
        self.assertTrue(isinstance(t, EbnfMap))
        self.assertTrue(isinstance(t.rules, OrderedDict))
        t2 = t.rules['top']
        self.assertTrue(isinstance(t2, EbnfMany))
        self.assertTrue(isinstance(t2.many, list))
        self.assertTrue(t2.many == [])

    def test_many_rule_list_2(self):
        t = reads(TAG_HEADER + "top: !many ['lt', 'gt']")
        self.assertTrue(isinstance(t, EbnfMap))
        self.assertTrue(isinstance(t.rules, OrderedDict))
        t2 = t.rules['top']
        self.assertTrue(isinstance(t2, EbnfMany))
        self.assertTrue(isinstance(t2.many, list))
        t3 = t2.many
        self.assertTrue(len(t3) == 2)
        self.assertTrue(isinstance(t3[0], EbnfStr))
        self.assertTrue(isinstance(t3[1], EbnfStr))
        self.assertTrue(t3[0].rule == 'lt')
        self.assertTrue(t3[1].rule == 'gt')

    def test_many_token_list_2(self):
        t = reads(TAG_HEADER + "top: !many [!token 'lt', !token 'gt']")
        self.assertTrue(isinstance(t, EbnfMap))
        self.assertTrue(isinstance(t.rules, OrderedDict))
        t2 = t.rules['top']
        self.assertTrue(isinstance(t2, EbnfMany))
        self.assertTrue(isinstance(t2.many, list))
        t3 = t2.many
        self.assertTrue(len(t3) == 2)
        self.assertTrue(isinstance(t3[0], EbnfToken))
        self.assertTrue(isinstance(t3[1], EbnfToken))
        self.assertTrue(t3[0].token == 'lt')
        self.assertTrue(t3[1].token == 'gt')
