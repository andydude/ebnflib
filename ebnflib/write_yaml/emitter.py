from yaml.emitter import (Emitter, ScalarAnalysis)

class EbnfYamlEmitter(Emitter):
    pass

    # def analyze_scalar(self, scalar):
    #     if isinstance(scalar, (list, tuple)):
    #         raise ValueError("expected scalar, but got {}".format(repr(scalar)))
    #     
    #     #return ScalarAnalysis(
    #     #    scalar=scalar,
    #     #    empty=False,
    #     #    multiline=False,
    #     #    allow_flow_plain=True,
    #     #    allow_block_plain=True,
    #     #    allow_single_quoted=False,
    #     #    allow_double_quoted=False,
    #     #    allow_block=True)
    #         
    #     return Emitter.analyze_scalar(self, scalar)
                      
