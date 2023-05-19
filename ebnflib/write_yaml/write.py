import io
import yaml
from .dumper import EbnfYamlDumper
from ebnflib.models import EbnfMap
from collections import OrderedDict

TAG_HEADER = "%TAG ! tag:drosoft.org/ebnf,2016:\n---\n"


def writes(obj):
    writer = io.StringIO()
    write(obj, writer)
    return writer.getvalue()
    
    
def write(obj, writer):
    assert isinstance(obj, EbnfMap)
    assert isinstance(obj.rules, OrderedDict)
    assert hasattr(writer, "write")
    EbnfYamlDumper.init_class(EbnfYamlDumper)
    writer.write(TAG_HEADER)
    yaml.dump(obj,
              stream=writer,
              Dumper=EbnfYamlDumper)
