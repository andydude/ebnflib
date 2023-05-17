#!/usr/bin/env python3
from unittest import TestCase
from collections import OrderedDict
from ebnflib.write_yaml.write import writes
from ebnflib.models import (
    EbnfTimes,
    EbnfStr,
    EbnfMap)

TAG_HEADER = "%TAG ! tag:drosoft.org/ebnf,2016:\n---\n"


class WriteYamlTimes(TestCase):

    def test_times_empty_list(self):
        t = EbnfMap(OrderedDict([
            ('top', EbnfTimes([]))]))
        s = writes(t)
        self.assertEqual(s, TAG_HEADER + "top: !times\n- []\n")

    def test_times_rule_list_1(self):
        t = EbnfMap(OrderedDict([
            ('top', EbnfTimes([EbnfStr('lt')]))]))
        s = writes(t)
        self.assertEqual(s, TAG_HEADER + "top: !times\n- lt\n")

    def test_times_rule_list_2(self):
        t = EbnfMap(OrderedDict([
            ('top', EbnfTimes([EbnfStr('lt'), 3]))]))
        s = writes(t)
        self.assertEqual(s, TAG_HEADER + "top: !times\n- lt\n- 3\n")

    def test_times_rule_list_3(self):
        t = EbnfMap(OrderedDict([
            ('top', EbnfTimes([EbnfStr('lt'), 3, 5]))]))
        s = writes(t)
        self.assertEqual(s, TAG_HEADER + "top: !times\n- lt\n- 3\n- 5\n")

    def test_times_rule_list_4(self):
        t = EbnfMap(OrderedDict([
            ('top', EbnfTimes([EbnfStr('lt'), 3, 5, True]))]))
        s = writes(t)
        self.assertEqual(s, TAG_HEADER + "top: !times\n- lt\n- 3\n- 5\n- true\n")

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
