import yaml
from collections import OrderedDict
from yaml.constructor import SafeConstructor


from ebnflib.models import (
    EbnfAlt,
    EbnfCharRange,
    EbnfCharSet,
    EbnfEmpty,
    EbnfGroup,
    EbnfMany,
    EbnfMany1,
    EbnfMap,
    EbnfMinus,
    EbnfOpt,
    EbnfRegExp,
    EbnfSepBy,
    EbnfSepEndBy,
    EbnfSeq,
    EbnfSpecial,
    EbnfStr,
    EbnfTimes,
    EbnfToken)


class EbnfYamlConstructor(SafeConstructor):
    
    @classmethod
    def init_class(cls, cls2):
        cls.init_ordered_dict(cls2.add_constructor)
        cls.init_constructors(cls2.add_constructor)

    @classmethod
    def init_ordered_dict(cls, add):
        # add(EbnfMap._tag,
        #     lambda constructor, node:
        #     OrderedDict(loader.construct_pairs(node)))
        add(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            lambda constructor, node:
            OrderedDict([
                (definiendum.rule, definiens)
                for definiendum, definiens in constructor.construct_pairs(node)
            ]))
            
    @classmethod
    def init_constructors(cls, add):
        add(EbnfAlt._tag, EbnfAlt.from_yaml)
        add(EbnfCharRange._tag, EbnfCharRange.from_yaml)
        add(EbnfCharSet._tag, EbnfCharSet.from_yaml)
        add(EbnfEmpty._tag, EbnfEmpty.from_yaml)
        add(EbnfGroup._tag, EbnfGroup.from_yaml)
        add(EbnfMany._tag, EbnfMany.from_yaml)
        add(EbnfMany1._tag, EbnfMany1.from_yaml)
        add(EbnfMinus._tag, EbnfMinus.from_yaml)
        add(EbnfOpt._tag, EbnfOpt.from_yaml)
        add(EbnfMap._tag, EbnfMap.from_yaml)
        add(EbnfRegExp._tag, EbnfRegExp.from_yaml)
        add(EbnfSepBy._tag, EbnfSepBy.from_yaml)
        add(EbnfSepEndBy._tag, EbnfSepEndBy.from_yaml)
        add(EbnfSeq._tag, EbnfSeq.from_yaml)
        add(EbnfSpecial._tag, EbnfSpecial.from_yaml)
        add(EbnfStr._tag, EbnfStr.from_yaml)
        add(EbnfTimes._tag, EbnfTimes.from_yaml)
        add(EbnfToken._tag, EbnfToken.from_yaml)
