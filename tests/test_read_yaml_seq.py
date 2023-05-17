#!/usr/bin/env python3
from unittest import TestCase
from collections import OrderedDict
from ebnflib.read_yaml.read import reads
from ebnflib.models import (
    EbnfSeq,
    EbnfMap,
    EbnfStr,
    EbnfToken)

TAG_HEADER = "%TAG ! tag:drosoft.org/ebnf,2016:\n---\n"


class ReadYamlSequence(TestCase):

    def test_seq_empty_list(self):
        t = reads(TAG_HEADER + "top: []")
        self.assertTrue(isinstance(t, EbnfMap))
        self.assertTrue(isinstance(t.rules, OrderedDict))
        t2 = t.rules['top']
        self.assertTrue(isinstance(t2, EbnfSeq))
        self.assertTrue(isinstance(t2.seq, list))
        self.assertTrue(t2.seq == [])

    def test_seq_rule_list_1(self):
        t = reads(TAG_HEADER + "top: ['lt']")
        self.assertTrue(isinstance(t, EbnfMap))
        self.assertTrue(isinstance(t.rules, OrderedDict))
        t2 = t.rules['top']
        self.assertTrue(isinstance(t2, EbnfSeq))
        self.assertTrue(isinstance(t2.seq, list))
        t3 = t2.seq
        self.assertTrue(len(t3) == 1)
        self.assertTrue(isinstance(t3[0], EbnfStr))
        self.assertTrue(t3[0].rule == 'lt')

    def test_seq_rule_list_2(self):
        t = reads(TAG_HEADER + "top: ['lt', 'gt']")
        self.assertTrue(isinstance(t, EbnfMap))
        self.assertTrue(isinstance(t.rules, OrderedDict))
        t2 = t.rules['top']
        self.assertTrue(isinstance(t2, EbnfSeq))
        self.assertTrue(isinstance(t2.seq, list))
        t3 = t2.seq
        self.assertTrue(len(t3) == 2)
        self.assertTrue(isinstance(t3[0], EbnfStr))
        self.assertTrue(isinstance(t3[1], EbnfStr))
        self.assertTrue(t3[0].rule == 'lt')
        self.assertTrue(t3[1].rule == 'gt')

    def test_seq_token_list_1(self):
        t = reads(TAG_HEADER + "top: [!token 'lt']")
        self.assertTrue(isinstance(t, EbnfMap))
        self.assertTrue(isinstance(t.rules, OrderedDict))
        t2 = t.rules['top']
        self.assertTrue(isinstance(t2, EbnfSeq))
        self.assertTrue(isinstance(t2.seq, list))
        t3 = t2.seq
        self.assertTrue(len(t3) == 1)
        self.assertTrue(isinstance(t3[0], EbnfToken))
        self.assertTrue(t3[0].token == 'lt')

    def test_seq_token_list_2(self):
        t = reads(TAG_HEADER + "top: [!token 'lt', !token 'gt']")
        self.assertTrue(isinstance(t, EbnfMap))
        self.assertTrue(isinstance(t.rules, OrderedDict))
        t2 = t.rules['top']
        self.assertTrue(isinstance(t2, EbnfSeq))
        self.assertTrue(isinstance(t2.seq, list))
        t3 = t2.seq
        self.assertTrue(len(t3) == 2)
        self.assertTrue(isinstance(t3[0], EbnfToken))
        self.assertTrue(isinstance(t3[1], EbnfToken))
        self.assertTrue(t3[0].token == 'lt')
        self.assertTrue(t3[1].token == 'gt')
