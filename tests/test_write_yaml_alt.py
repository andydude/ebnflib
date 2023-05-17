#!/usr/bin/env python3
from unittest import TestCase
from collections import OrderedDict
from ebnflib.write_yaml.write import writes
from ebnflib.models import (
    EbnfAlt,
    EbnfStr,
    EbnfMap)

TAG_HEADER = "%TAG ! tag:drosoft.org/ebnf,2016:\n---\n"


class WriteYamlAlt(TestCase):

    def test_alt_empty_list(self):
        t = EbnfMap(OrderedDict([
            ('top', EbnfAlt([]))]))
        s = writes(t)
        self.assertEqual(s, TAG_HEADER + "top: !alt []\n")

    def test_alt_rule_list_1(self):
        t = EbnfMap(OrderedDict([
            ('top', EbnfAlt([EbnfStr('lt')]))]))
        s = writes(t)
        self.assertEqual(s, TAG_HEADER + "top: !alt\n- lt\n")

    def test_alt_rule_list_2(self):
        t = EbnfMap(OrderedDict([
            ('top', EbnfAlt([EbnfStr('lt'),
                             EbnfStr('gt')]))]))
        s = writes(t)
        self.assertEqual(s, TAG_HEADER + "top: !alt\n- lt\n- gt\n")

    # def test_empty_bool_true(self):
    #     t = EbnfMap(OrderedDict([
    #         ('top', EbnfEmpty('true'))]))
    #     s = writes(t)
    #     self.assertEqual(s, TAG_HEADER + "top: !empty 'true'\n")
    # 
    # def test_empty_bool_false(self):
    #     t = EbnfMap(OrderedDict([
    #         ('top', EbnfEmpty('false'))]))
    #     s = writes(t)
    #     self.assertEqual(s, TAG_HEADER + "top: !empty 'false'\n")
    # 
    # def test_empty_empty_str(self):
    #     t = EbnfMap(OrderedDict([
    #         ('top', EbnfEmpty(''))]))
    #     s = writes(t)
    #     self.assertEqual(s, TAG_HEADER + "top: !empty ''\n")
    # 
    # def test_empty_comment(self):
    #     t = EbnfMap(OrderedDict([
    #         ('top', EbnfEmpty('hello'))]))
    #     s = writes(t)
    #     self.assertEqual(s, TAG_HEADER + "top: !empty 'hello'\n")
