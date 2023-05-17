#!/usr/bin/env python3
from unittest import TestCase
from collections import OrderedDict
from ebnflib.write_yaml.write import writes
from ebnflib.models import (
    EbnfSpecial,
    EbnfMap)

TAG_HEADER = "%TAG ! tag:drosoft.org/ebnf,2016:\n---\n"


class WriteYamlScalars(TestCase):

    # def test_always(self):
    #     self.assertTrue(True)
    #
    # def test_special_none(self):
    #     t = EbnfMap(OrderedDict([
    #         ('top', EbnfSpecial(None))]))
    #     s = writes(t)
    #     self.assertEqual(s, TAG_HEADER + "top: !special null\n")

    def test_special_null(self):
        t = EbnfMap(OrderedDict([
            ('top', EbnfSpecial('null'))]))
        s = writes(t)
        self.assertEqual(s, TAG_HEADER + "top: !special 'null'\n")

    def test_special_bool_true(self):
        t = EbnfMap(OrderedDict([
            ('top', EbnfSpecial('true'))]))
        s = writes(t)
        self.assertEqual(s, TAG_HEADER + "top: !special 'true'\n")

    def test_special_bool_false(self):
        t = EbnfMap(OrderedDict([
            ('top', EbnfSpecial('false'))]))
        s = writes(t)
        self.assertEqual(s, TAG_HEADER + "top: !special 'false'\n")

    def test_special_special_str(self):
        t = EbnfMap(OrderedDict([
            ('top', EbnfSpecial(''))]))
        s = writes(t)
        self.assertEqual(s, TAG_HEADER + "top: !special ''\n")

    def test_special_comment(self):
        t = EbnfMap(OrderedDict([
            ('top', EbnfSpecial('hello'))]))
        s = writes(t)
        self.assertEqual(s, TAG_HEADER + "top: !special 'hello'\n")
