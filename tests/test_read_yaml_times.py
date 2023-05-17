#!/usr/bin/env python3
from unittest import TestCase
from collections import OrderedDict
from ebnflib.read_yaml.read import reads
from ebnflib.models import (
    EbnfTimes,
    EbnfStr,
    EbnfMap)

TAG_HEADER = "%TAG ! tag:drosoft.org/ebnf,2016:\n---\n"


class ReadYamlScalars(TestCase):

    def test_always(self):
        self.assertTrue(True)

    def test_times_empty_list(self):
        t = reads(TAG_HEADER + "top: !times []")
        self.assertTrue(isinstance(t, EbnfMap))
        self.assertTrue(isinstance(t.rules, OrderedDict))
        t2 = t.rules['top']
        self.assertTrue(isinstance(t2, EbnfTimes))

    def test_times_empty_list(self):
        t = reads(TAG_HEADER + "top: !times ['lt']")
        self.assertTrue(isinstance(t, EbnfMap))
        self.assertTrue(isinstance(t.rules, OrderedDict))
        t2 = t.rules['top']
        self.assertTrue(isinstance(t2, EbnfTimes))

    def test_times_rule_list_2(self):
        t = reads(TAG_HEADER + "top: !times ['lt', 3]")
        self.assertTrue(isinstance(t, EbnfMap))
        self.assertTrue(isinstance(t.rules, OrderedDict))
        t2 = t.rules['top']
        self.assertTrue(isinstance(t2, EbnfTimes))
        self.assertTrue(isinstance(t2.times, EbnfStr))
        self.assertTrue(t2.times.rule == 'lt')
        self.assertTrue(t2.minimum == 3)
        self.assertTrue(t2.maximum == 3)

    def test_times_rule_list_3(self):
        t = reads(TAG_HEADER + "top: !times ['lt', 3, 5]")
        self.assertTrue(isinstance(t, EbnfMap))
        self.assertTrue(isinstance(t.rules, OrderedDict))
        t2 = t.rules['top']
        self.assertTrue(isinstance(t2, EbnfTimes))
        self.assertTrue(isinstance(t2.times, EbnfStr))
        self.assertTrue(t2.times.rule == 'lt')
        self.assertTrue(t2.minimum == 3)
        self.assertTrue(t2.maximum == 5)

    def test_times_rule_list_4(self):
        t = reads(TAG_HEADER + "top: !times ['lt', 3, 5, true]")
        self.assertTrue(isinstance(t, EbnfMap))
        self.assertTrue(isinstance(t.rules, OrderedDict))
        t2 = t.rules['top']
        self.assertTrue(isinstance(t2, EbnfTimes))
        self.assertTrue(isinstance(t2.times, EbnfStr))
        self.assertTrue(isinstance(t2.times.rule, str))
        self.assertTrue(isinstance(t2.minimum, int))
        self.assertTrue(isinstance(t2.maximum, int))
        self.assertTrue(isinstance(t2.lazy, bool))
        self.assertTrue(t2.times.rule == 'lt')
        self.assertTrue(t2.minimum == 3)
        self.assertTrue(t2.maximum == 5)
        self.assertTrue(t2.lazy == True)

