from collections import OrderedDict
from yaml.representer import SafeRepresenter

from ebnflib.models import (
    EbnfAlt,
    EbnfAny,
    EbnfBase,
    EbnfCharRange,
    EbnfCharSet,
    EbnfGroup,
    EbnfMany,
    EbnfMany1,
    EbnfMap,
    EbnfMinus,
    EbnfOpt,
    EbnfRegExp,
    EbnfSepBy,
    EbnfSepEndBy,
    EbnfSpecial,
    EbnfStr,
    EbnfSeq,
    EbnfEmpty,
    EbnfTimes,
    EbnfToken)


class EbnfYamlRepresenter(SafeRepresenter):

    # These must be of the form !tag 'string'
    yaml_scalar_types = [
        'EbnfComment',
        'EbnfEmpty',
        'EbnfRegExp',
        'EbnfSpecial',
        'EbnfStr',
        'EbnfToken',
    ]

    # These must be of the form !tag ['a', 'b']
    yaml_sequence_types = [
        'EbnfAlt',
        'EbnfCharRange',
        'EbnfCharSet',
        'EbnfGroup',
        'EbnfMany',
        'EbnfMany1',
        'EbnfMinus',
        'EbnfOpt',
        'EbnfSepBy',
        'EbnfSepEndBy',
        'EbnfSeq',
        'EbnfTimes',
    ]

    # def get_alias_key(self):
    #     return None
    # def set_alias_key(self, key):
    #     return
    # alias_key = property(get_alias_key,
    #                      set_alias_key)
    
    def get_ser_nodes(self):
        return {}
    def set_ser_nodes(self, key):
        return
    serialized_nodes = property(get_ser_nodes,
                                set_ser_nodes)

    def get_rep_objects(self):
        return {}
    def set_rep_objects(self, key):
        return
    represented_objects = property(get_rep_objects,
                                   set_rep_objects)

    
    def ignore_aliases(self, data):
        return True

    # def represent_data(self, data):
    #     # if type(data).__name__ in self.yaml_scalar_types:
    #     #     # print("# repdata data =", data)
    #     #     node = type(data).to_yaml(self, data)
    #     #     return node
    #     # elif type(data).__name__ in self.yaml_sequence_types:
    #     #     # print("# repdata data[] = ", data)
    #     #     node = type(data).to_yaml(self, data)
    #     #     return node
    #     # else:
    #     node = super().represent_data(data)
    #     return node
            
    @classmethod
    def init_class(cls, cls2):
        cls.init_ordered_dict(cls2.add_representer)
        cls.init_representers(cls2.add_representer)

    @classmethod
    def init_ordered_dict(cls, add):
        add(bool,
            SafeRepresenter.represent_bool)
        add(type(None),
            SafeRepresenter.represent_none)
        add(OrderedDict,
            lambda representer, self:
            representer.represent_dict(
                self.items()))


    @classmethod
    def init_representers(cls, add):
        add(EbnfAlt, EbnfAlt.to_yaml)
        add(EbnfCharRange, EbnfCharRange.to_yaml)
        add(EbnfCharSet, EbnfCharSet.to_yaml)
        add(EbnfEmpty, EbnfEmpty.to_yaml)
        add(EbnfGroup, EbnfGroup.to_yaml)
        add(EbnfMany, EbnfMany.to_yaml)
        add(EbnfMany1, EbnfMany1.to_yaml)
        add(EbnfMap, EbnfMap.to_yaml)
        add(EbnfMinus, EbnfMinus.to_yaml)
        add(EbnfOpt, EbnfOpt.to_yaml)
        add(EbnfRegExp, EbnfRegExp.to_yaml)
        add(EbnfSepBy, EbnfSepBy.to_yaml)
        add(EbnfSepEndBy, EbnfSepEndBy.to_yaml)
        add(EbnfSeq, EbnfSeq.to_yaml)
        add(EbnfSpecial, EbnfSpecial.to_yaml)
        add(EbnfStr, EbnfStr.to_yaml)
        add(EbnfTimes, EbnfTimes.to_yaml)
        add(EbnfToken, EbnfToken.to_yaml)

        # def add(x, y):
        #     lambda x, y: self.builtin_tags[x] = y
        # EbnfDumper.init_ebnf_constructors(add)

    # def represent_ordered_dict(self, data):
    #     items = [[key, value] for key, value in data.items()]
    #     return self.represent_sequence(EbnfMap._tag, [items])
