#!/usr/bin/env python3
from unittest import TestCase
from collections import OrderedDict
from ebnflib.write_yaml.write import writes
from ebnflib.models import (
    EbnfEmpty,
    EbnfMap)

TAG_HEADER = "%TAG ! tag:drosoft.org/ebnf,2016:\n---\n"


class WriteYamlScalars(TestCase):

    # def test_always(self):
    #     self.assertTrue(True)
    #
    # def test_empty_none(self):
    #     t = EbnfMap(OrderedDict([
    #         ('top', EbnfEmpty(None))]))
    #     s = writes(t)
    #     self.assertEqual(s, TAG_HEADER + "top: !empty null\n")

    def test_empty_null(self):
        t = EbnfMap(OrderedDict([
            ('top', EbnfEmpty('null'))]))
        s = writes(t)
        self.assertEqual(s, TAG_HEADER + "top: !empty 'null'\n")

    def test_empty_bool_true(self):
        t = EbnfMap(OrderedDict([
            ('top', EbnfEmpty('true'))]))
        s = writes(t)
        self.assertEqual(s, TAG_HEADER + "top: !empty 'true'\n")

    def test_empty_bool_false(self):
        t = EbnfMap(OrderedDict([
            ('top', EbnfEmpty('false'))]))
        s = writes(t)
        self.assertEqual(s, TAG_HEADER + "top: !empty 'false'\n")

    def test_empty_empty_str(self):
        t = EbnfMap(OrderedDict([
            ('top', EbnfEmpty(''))]))
        s = writes(t)
        self.assertEqual(s, TAG_HEADER + "top: !empty ''\n")

    def test_empty_comment(self):
        t = EbnfMap(OrderedDict([
            ('top', EbnfEmpty('hello'))]))
        s = writes(t)
        self.assertEqual(s, TAG_HEADER + "top: !empty 'hello'\n")
