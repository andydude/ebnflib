import io
import yaml
from .loader import EbnfYamlLoader
from ebnflib.utils import init_crossrefs
from ebnflib.models import EbnfMap
from collections import OrderedDict


def reads(s):
    assert isinstance(s, str)
    reader = io.StringIO(s)
    return read(reader)


def read(reader):
    assert hasattr(reader, "read")
    init_crossrefs()
    rules = yaml.load(
        stream=reader,
        Loader=EbnfYamlLoader)
    if isinstance(rules, EbnfMap):
        return rules
    elif isinstance(rules, OrderedDict):
        assert isinstance(rules, OrderedDict)
        rules = EbnfMap(rules=rules)
        assert isinstance(rules, EbnfMap)
        return rules
    else:
        raise ValueError
