from yaml.loader import SafeLoader
from .constructor import EbnfYamlConstructor


class EbnfYamlLoader(SafeLoader, EbnfYamlConstructor):

    def __init__(self, stream):
        SafeLoader.__init__(self, stream=stream)
        EbnfYamlConstructor.init_class(type(self))
