from yaml.dumper import SafeDumper, Dumper
from .representer import EbnfYamlRepresenter
from .emitter import EbnfYamlEmitter

class EbnfYamlDumper(SafeDumper, EbnfYamlRepresenter):

    def __init__(
            self,
            stream,
            allow_unicode=None,
            canonical=False,
            default_flow_style=False,
            default_style=None,
            encoding=None,
            explicit_end=None,
            explicit_start=None,
            indent=None,
            line_break=None,
            sort_keys=False,
            tags=None,
            version=None,
            width=None):
        SafeDumper.__init__(
            self,
            stream,
            allow_unicode=allow_unicode,
            canonical=canonical,
            default_flow_style=default_flow_style,
            default_style=default_style,
            encoding=encoding,
            explicit_end=explicit_end,
            explicit_start=explicit_start,
            indent=indent,
            line_break=line_break,
            sort_keys=sort_keys,
            tags=tags,
            version=version,
            width=width)
        EbnfYamlRepresenter.init_class(EbnfYamlRepresenter)
        self.sort_keys = False
