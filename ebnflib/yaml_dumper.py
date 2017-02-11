import collections
import json
import logging
import yaml
logger = logging.getLogger(__name__)

from ebnflib.models import (
    EbnfAlt,
    EbnfGroup,
    EbnfMany,
    EbnfMany1,
    EbnfMap,
    EbnfMinus,
    EbnfOpt,
    EbnfRegExp,
    EbnfSeq,
    EbnfSpecial,
    EbnfStr,
    EbnfTimes,
    EbnfToken)

def to_unicode(s):
    return s

class EbnfDumper(object):

    builtin_dumpers = {
        'OrderedDict': EbnfMap,
        'dict': EbnfMap,
        'list': EbnfSeq,
        'str': EbnfStr,
        'unicode': EbnfStr,
    }

    builtin_identity = [
        'ScalarNode',
        'SequenceNode',
    ]

    builtin_tags = {
        'tag:yaml.org,2002:str': EbnfStr,
        'tag:yaml.org,2002:seq': EbnfSeq,
        'tag:yaml.org,2002:map': EbnfMap,
    }
    
    def __init__(self, method='to_ebnf'):
        def add(x, y):
            self.builtin_tags[x] = y
        EbnfDumper.init_ebnf_constructors(add)
        self.method = method

    @staticmethod
    def init_once():
        def dict_representer(dumper, data):
            return dumper.represent_dict(data.iteritems())
        def dict_constructor(loader, node):
            return collections.OrderedDict(loader.construct_pairs(node))
        yaml.constructor.Constructor.add_constructor(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, dict_constructor)
        yaml.representer.Representer.add_representer(
            collections.OrderedDict, dict_representer)
        EbnfDumper.init_ebnf_constructors(yaml.constructor.Constructor.add_constructor)
        EbnfDumper.init_ebnf_representers(yaml.representer.Representer.add_representer)

    def convert(self, obj):
        cls = type(obj)
        typename = cls.__name__
        if typename in self.builtin_identity and obj._tag == 'tag:yaml.org,2002:str':
            return to_unicode(obj.value)
        elif typename in self.builtin_identity and obj._tag in self.builtin_tags:
            cls = self.builtin_tags[obj._tag]
            
            # Same
            parent = yaml.constructor.Constructor()
            instance = cls(parent, obj)
            converted = getattr(instance, self.method)(self)
            return to_unicode(converted)
        elif typename in self.builtin_dumpers:
            cls = self.builtin_dumpers[typename]

            # Same
            parent = yaml.constructor.Constructor()
            try:
                instance = cls(obj)
            except Exception as err:
                logger.error(repr(err), exc_info=True)
                #print("obj = %s" % repr(obj))
                #print("cls = %s" % repr(cls))
                #print("parent = %s" % repr(parent))
                #print("instance = %s" % repr(instance))
            converted = getattr(instance, self.method)(self)
            return to_unicode(converted)
        elif typename.startswith('Ebnf'):
            return to_unicode(obj.to_ebnf(self))
        else:
            if hasattr(obj, 'value'):
                return to_unicode(obj.value)
            else:
                return to_unicode(obj)

    @staticmethod
    def init_ebnf_constructors(add_constructor):
        add_constructor(EbnfAlt._tag, EbnfAlt.from_yaml)
        add_constructor(EbnfOpt._tag, EbnfOpt.from_yaml)
        add_constructor(EbnfToken._tag, EbnfToken.from_yaml)
        add_constructor(EbnfMinus._tag, EbnfMinus.from_yaml)
        add_constructor(EbnfTimes._tag, EbnfTimes.from_yaml)
        add_constructor(EbnfRegExp._tag, EbnfRegExp.from_yaml)
        add_constructor(EbnfGroup._tag, EbnfGroup.from_yaml)
        add_constructor(EbnfSpecial._tag, EbnfSpecial.from_yaml)
        add_constructor(EbnfMany._tag, EbnfMany.from_yaml)
        add_constructor(EbnfMany1._tag, EbnfMany1.from_yaml)
    
    @staticmethod
    def init_ebnf_representers(add_representer):
        add_representer(EbnfAlt, EbnfAlt.to_yaml)
        add_representer(EbnfOpt, EbnfOpt.to_yaml)
        add_representer(EbnfToken, EbnfToken.to_yaml)
        add_representer(EbnfMinus, EbnfMinus.to_yaml)
        add_representer(EbnfTimes, EbnfTimes.to_yaml)
        add_representer(EbnfRegExp, EbnfRegExp.to_yaml)
        add_representer(EbnfSpecial, EbnfSpecial.to_yaml)
        add_representer(EbnfGroup, EbnfGroup.to_yaml)
        add_representer(EbnfMany, EbnfMany.to_yaml)
        add_representer(EbnfMany1, EbnfMany1.to_yaml)

def main():
    from ebnflib.utils import init_crossrefs
    import sys
    import logging.config
    logging.basicConfig(filename='/dev/stdout')
    init_crossrefs()
    filename = sys.argv[1]
    with open(filename) as fp:
        source = fp.read()

    EbnfDumper.init_once()
    dumper = EbnfDumper()
    data = yaml.load(source)
    print("---")
    print(dumper.convert(data))
    print("---")
    print(yaml.dump(data, default_flow_style=False))
    
if __name__ == '__main__':
    main()
