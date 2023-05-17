#!/usr/bin/env python3
from unittest import TestCase
from collections import OrderedDict
from ebnflib.read_yaml.read import reads
from ebnflib.models import (
    EbnfGroup,
    EbnfMap,
    EbnfStr,
    EbnfToken)

TAG_HEADER = "%TAG ! tag:drosoft.org/ebnf,2016:\n---\n"


class ReadYamlScalars(TestCase):

    def test_always(self):
        self.assertTrue(True)

    def test_group_rule(self):
        # discouraged, but allowed, should be !group [digit]
        t = reads(TAG_HEADER + "top: !group digit")
        self.assertTrue(isinstance(t, EbnfMap))
        self.assertTrue(isinstance(t.rules, OrderedDict))
        t2 = t.rules['top']
        print(repr(t2))
        self.assertTrue(isinstance(t2, EbnfGroup))
        self.assertTrue(isinstance(t2.group, EbnfStr))
        self.assertTrue(t2.group.rule == 'digit')

    def test_group_empty_list(self):
        t = reads(TAG_HEADER + "top: !group []")
        self.assertTrue(isinstance(t, EbnfMap))
        self.assertTrue(isinstance(t.rules, OrderedDict))
        t2 = t.rules['top']
        self.assertTrue(isinstance(t2, EbnfGroup))
        self.assertTrue(isinstance(t2.group, list))
        self.assertTrue(t2.group == [])

    def test_group_rule_list_1(self):
        t = reads(TAG_HEADER + "top: !group ['lt']")
        self.assertTrue(isinstance(t, EbnfMap))
        self.assertTrue(isinstance(t.rules, OrderedDict))
        t2 = t.rules['top']
        self.assertTrue(isinstance(t2, EbnfGroup))
        self.assertTrue(isinstance(t2.group, list))
        t3 = t2.group
        self.assertTrue(len(t3) == 1)
        self.assertTrue(isinstance(t3[0], EbnfStr))
        self.assertTrue(t3[0].rule == 'lt')

    def test_group_rule_list_2(self):
        t = reads(TAG_HEADER + "top: !group ['lt', 'gt']")
        self.assertTrue(isinstance(t, EbnfMap))
        self.assertTrue(isinstance(t.rules, OrderedDict))
        t2 = t.rules['top']
        self.assertTrue(isinstance(t2, EbnfGroup))
        self.assertTrue(isinstance(t2.group, list))
        t3 = t2.group
        self.assertTrue(len(t3) == 2)
        self.assertTrue(isinstance(t3[0], EbnfStr))
        self.assertTrue(isinstance(t3[1], EbnfStr))
        self.assertTrue(t3[0].rule == 'lt')
        self.assertTrue(t3[1].rule == 'gt')

    def test_group_token_list_1(self):
        t = reads(TAG_HEADER + "top: !group [!token 'lt']")
        self.assertTrue(isinstance(t, EbnfMap))
        self.assertTrue(isinstance(t.rules, OrderedDict))
        t2 = t.rules['top']
        self.assertTrue(isinstance(t2, EbnfGroup))
        self.assertTrue(isinstance(t2.group, list))
        t3 = t2.group
        self.assertTrue(len(t3) == 1)
        self.assertTrue(isinstance(t3[0], EbnfToken))
        self.assertTrue(t3[0].token == 'lt')

    def test_group_token_list_2(self):
        t = reads(TAG_HEADER + "top: !group [!token 'lt', !token 'gt']")
        self.assertTrue(isinstance(t, EbnfMap))
        self.assertTrue(isinstance(t.rules, OrderedDict))
        t2 = t.rules['top']
        self.assertTrue(isinstance(t2, EbnfGroup))
        self.assertTrue(isinstance(t2.group, list))
        t3 = t2.group
        self.assertTrue(len(t3) == 2)
        self.assertTrue(isinstance(t3[0], EbnfToken))
        self.assertTrue(isinstance(t3[1], EbnfToken))
        self.assertTrue(t3[0].token == 'lt')
        self.assertTrue(t3[1].token == 'gt')
