#!/usr/bin/env python3
from unittest import TestCase
from collections import OrderedDict
from ebnflib.write_yaml.write import writes
from ebnflib.models import (
    EbnfMany,
    EbnfStr,
    EbnfMap)

TAG_HEADER = "%TAG ! tag:drosoft.org/ebnf,2016:\n---\n"


class WriteYamlMany(TestCase):

    def test_many_empty_list(self):
        t = EbnfMap(OrderedDict([
            ('top', EbnfMany([]))]))
        s = writes(t)
        self.assertEqual(s, TAG_HEADER + "top: !many []\n")

    def test_many_rule_list_1(self):
        t = EbnfMap(OrderedDict([
            ('top', EbnfMany([EbnfStr('lt')]))]))
        s = writes(t)
        self.assertEqual(s, TAG_HEADER + "top: !many\n- lt\n")

    def test_many_rule_list_2(self):
        t = EbnfMap(OrderedDict([
            ('top', EbnfMany([EbnfStr('lt'),
                              EbnfStr('gt')]))]))
        s = writes(t)
        self.assertEqual(s, TAG_HEADER + "top: !many\n- lt\n- gt\n")

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
