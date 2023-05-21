import six
from typing import Dict, List
from dataclasses import dataclass
from collections import OrderedDict


class EbnfBase:
    pass


class EbnfAny(EbnfBase):
    '''
    Instances of this class represent ISO 14977 SS 4.10 syntactic-primary.

    Syntactic-primary only allows the following members:

    * EbnfEmpty		(empty-sequence)
    * EbnfGroup		(grouped-sequence)
    * EbnfMany		(repeated-sequence)
    * EbnfMany1
    * EbnfOpt		(optional-sequence)
    * EbnfSpecial	(special-sequence)
    * EbnfStr		(meta-identifier)
    * EbnfToken		(terminal-string)

    but using a grouped-sequence, one can include the others as children
    of the grouped-sequence, and thus more are allowed. The standard requires
    that these are strictly represented, perhaps soon we will.

    EbnfMany1 is not a fundamental structure. It can be represented as:

    .. code:: python

       EbnfMany1(many1=obj) ==
       EbnfGroup(
         group=EbnfSeq(
           seq=[obj, EbnfMany(many=obj)]
         )
       )
    '''

    @classmethod
    def __new__(cls, obj):
        from collections.abc import Mapping, Sequence
        if isinstance(obj, Sequence):
            return EbnfSeq(obj)
        elif isinstance(obj, six.string_types):
            return EbnfStr(obj)
        elif not isinstance(obj, Mapping):
            raise TypeError

        if 'alt' in obj:
            return EbnfAlt(**obj)
        elif 'comment' in obj:
            return EbnfComment(**obj)
        elif 'empty' in obj:
            return EbnfEmpty(**obj)
        elif 'group' in obj:
            return EbnfGroup(**obj)
        elif 'many' in obj:
            return EbnfMany(**obj)
        elif 'many1' in obj:
            return EbnfMany1(**obj)
        elif 'rules' in obj:
            return EbnfMap(**obj)
        elif 'minuend' in obj:
            return EbnfMinus(**obj)
        elif 'opt' in obj:
            return EbnfOpt(**obj)
        elif 'regexp' in obj:
            return EbnfRegExp(**obj)
        elif 'sepby' in obj:
            return EbnfSepBy(**obj)
        elif 'sebendby' in obj:
            return EbnfSepEndBy(**obj)
        elif 'seq' in obj:
            return EbnfSeq(**obj)
        elif 'special' in obj:
            return EbnfSpecial(**obj)
        elif 'rule' in obj:
            return EbnfStr(**obj)
        elif 'times' in obj:
            return EbnfTimes(**obj)
        elif 'token' in obj:
            return EbnfToken(**obj)
        else:
            raise ValueError(obj)


@dataclass
class EbnfAlt(EbnfBase):
    '''
    Instances of this class represent ISO 14977 SS 4.4 definitions-list.

    The EBNF associated with definitions-list is as follows

    .. code:: ebnf

       definitions list
           = single definition,
           {'|', single definition};

    Definitions-list can be represented in YAML as follows

    .. code:: yaml

       definitions list:
         - single definition
         - !many
           - !token '|'
           - single definition
    '''
    alt: List[EbnfBase]
    _tag = 'tag:drosoft.org/ebnf,2016:alt'

    def __init__(self, alt):
        object.__init__(self)
        assert isinstance(alt, list)
        self.alt = alt

    def __iter__(self):
        for item in self.alt:
            yield item

    def to_ebnf(self, converter):
        '''
        Returns a string with the EBNF representations of self.alt,
        interpersed with virtical bars ('|').
        '''
        converted = '\n\t| '.join([converter.convert(value)
                                   for value in self.alt])
        if len(converted) < 80:
            converted = converted.replace('\n\t', ' ')
        return converted

    def to_lisp(self):
        from hy.models import Expression, Symbol
        args = list(map(
            lambda self: self.to_lisp(), self.alt))
        return Expression(
            [Symbol("or")] + args)

    @classmethod
    def from_yaml(cls, constructor, node, deep=False):
        alt = [constructor.construct_object(child, deep=deep)
               for child in node.value]
        return cls(alt=alt)

    @classmethod
    def to_yaml(cls, representer, self):
        from .utils import short_tag
        return representer.represent_sequence(
            short_tag(cls._tag), self.alt)


@dataclass
class EbnfCharRange(EbnfBase):
    first: EbnfBase
    last: EbnfBase
    _tag = 'tag:drosoft.org/ebnf,2016:charrange'

    def __init__(self, first, last):
        object.__init__(self)
        assert isinstance(first, EbnfToken)
        assert isinstance(last, EbnfToken)
        self.first = first
        self.last = last

    def __iter__(self):
        yield self.first
        yield self.last

    @classmethod
    def from_yaml(cls, constructor, node, deep=False):
        if isinstance(node.value, EbnfBase):
            # print(repr(node.value))
            raise ValueError(node.value)
        elif isinstance(node.value, (list, tuple)):
            args = [constructor.construct_object(child, deep=deep)
                    for child in node.value]
            return cls(first=args[0],
                       last=args[1])

    @classmethod
    def to_yaml(cls, representer, self):
        from .utils import short_tag
        return representer.represent_sequence(
            short_tag(cls._tag),
            [self.first,
             self.last])


@dataclass
class EbnfCharSet(EbnfBase):
    chars: str
    negative: bool
    _tag = 'tag:drosoft.org/ebnf,2016:charset'

    def __init__(self, chars, negative=False):
        object.__init__(self)
        assert isinstance(chars, str)
        self.chars = chars
        self.negative = negative

    def __iter__(self):
        yield self.chars
        yield self.negative

    def to_lisp(self):
        from hy.models import (Expression, Symbol)
        return Expression(
            [Symbol("char-set"), str(self.chars)])

    @classmethod
    def from_yaml(cls, constructor, node, deep=False):
        if isinstance(node.value, EbnfBase):
            return cls(chars=node.value,
                       negative=False)
        elif isinstance(node.value, (list, tuple)):
            args = [constructor.construct_object(child, deep=deep)
                    for child in node.value]
            return cls(chars=args[0],
                       negative=args[1])

    @classmethod
    def to_yaml(cls, representer, self):
        from .utils import short_tag
        return representer.represent_sequence(
            short_tag(cls._tag),
            self.chars)


@dataclass
class EbnfComment(EbnfBase):
    '''
    Instances of this class represent ISO 14977 comments.

    .. code:: ebnf

       (* This is a comment. *)

    Comments can be represented in YAML as

    .. code:: yaml

       !comment This is a comment.

    if you want to represent an EBNF comment, or

    .. code:: yaml

       # This is a comment.

    if you want the comment to disappear after processing.
    '''
    comment: str
    _tag = 'tag:drosoft.org/ebnf,2016:comment'

    def __init__(self, comment):
        object.__init__(self)
        self.comment = comment


@dataclass
class EbnfEmpty(EbnfBase):
    '''
    '''
    empty: str = ''
    _tag = 'tag:drosoft.org/ebnf,2016:empty'

    def __init__(self, empty=''):
        object.__init__(self)
        self.empty = empty

    @classmethod
    def from_yaml(cls, constructor, node, deep=False):
        return cls(empty=node.value)

    @classmethod
    def to_yaml(cls, representer, self):
        from .utils import short_tag
        return representer.represent_scalar(
            short_tag(cls._tag), self.empty)


@dataclass
class EbnfGroup(EbnfBase):
    '''
    '''
    group: List[EbnfBase]
    _tag = 'tag:drosoft.org/ebnf,2016:group'

    def __init__(self, group):
        object.__init__(self)
        self.group = group

    def __iter__(self):
        for item in self.group:
            yield item

    def to_ebnf(self, parent):
        if isinstance(self.group, EbnfBase):
            inner = parent.convert(self.group)
            return '( %s )' % (inner)
        elif isinstance(self.group, (list, tuple)):
            inner = ' '.join(map(parent.convert, self.group))
            return '( %s )' % (inner)

    @classmethod
    def from_yaml(cls, constructor, node, deep=False):
        if isinstance(node.value, str):
            return cls(group=EbnfStr(node.value))
        elif isinstance(node.value, EbnfBase):
            return cls(group=node.value)
        elif isinstance(node.value, (list, tuple)):
            group = [constructor.construct_object(child, deep=deep)
                     for child in node.value]
            return cls(group=group)

    @classmethod
    def to_yaml(cls, representer, self):
        from .utils import short_tag
        if isinstance(self.group, str):
            return representer.represent_scalar(
                short_tag(cls._tag), self.group)
        elif isinstance(self.group, EbnfStr):
            return representer.represent_scalar(
                short_tag(cls._tag), self.group.rule)
        elif isinstance(self.group, EbnfBase):
            return representer.represent_scalar(
                short_tag(cls._tag), self.group)
        elif isinstance(self.group, (list, tuple)):
            return representer.represent_sequence(
                short_tag(cls._tag), self.group)
        else:
            raise ValueError(type(self.group))


@dataclass
class EbnfMany(EbnfBase):
    '''
    '''
    many: List[EbnfBase]
    lazy: bool
    _tag = 'tag:drosoft.org/ebnf,2016:many'

    def __init__(self, many, lazy=False):
        object.__init__(self)
        self.many = many
        self.lazy = lazy

    def __iter__(self):
        yield self.many
        yield self.lazy

    def to_lisp(self):
        from hy.models import (Expression, Symbol)
        args = list(map(
            lambda self: self.to_lisp(),
            self.many))
        return Expression(
            [Symbol("*")] + args)

    @classmethod
    def from_yaml(cls, constructor, node, deep=False):
        if isinstance(node.value, str):
            return cls(many=EbnfStr(node.value))
        elif isinstance(node.value, EbnfBase):
            return cls(many=node.value)
        elif isinstance(node.value, (list, tuple)):
            many = [constructor.construct_object(child, deep=deep)
                    for child in node.value]
            return cls(many=many)
        else:
            raise ValueError(node, type(node), repr(node))

    def to_ebnf(self, parent):
        converted = parent.convert(self.many)
        return "{ %s }" % converted

    @classmethod
    def to_yaml(cls, representer, self):
        from .utils import short_tag
        if isinstance(self.many, str):
            return representer.represent_scalar(
                short_tag(cls._tag), self.many)
        elif isinstance(self.many, EbnfStr):
            return representer.represent_scalar(
                short_tag(cls._tag), self.many.rule)
        elif isinstance(self.many, EbnfBase):
            return representer.represent_scalar(
                short_tag(cls._tag), self.many)
        elif isinstance(self.many, (list, tuple)):
            return representer.represent_sequence(
                short_tag(cls._tag), self.many)


@dataclass
class EbnfMany1(EbnfBase):
    '''
    '''
    many1: List[EbnfBase]
    lazy: bool
    _tag = 'tag:drosoft.org/ebnf,2016:many1'

    def __init__(self, many1, lazy=False):
        object.__init__(self)
        self.many1 = many1
        self.lazy = lazy

    def __iter__(self):
        yield self.many1
        yield self.lazy

    def to_lisp(self):
        from hy.models import (Expression, Symbol)
        args = list(map(
            lambda self: self.to_lisp(),
            self.many))
        return Expression(
            [Symbol("+")] + args)

    @classmethod
    def from_yaml(cls, constructor, node, deep=False):
        if isinstance(node.value, str):
            return cls(many1=EbnfStr(node.value))
        elif isinstance(node.value, EbnfBase):
            return cls(many1=node.value)
        elif isinstance(node.value, (list, tuple)):
            many1 = [constructor.construct_object(child, deep=deep)
                     for child in node.value]
            return cls(many1=many1)

    def to_ebnf(self, parent):
        converted = parent.convert(self.many1)
        return "%s, { %s }" % (converted, converted)

    @classmethod
    def to_yaml(cls, representer, self):
        from .utils import short_tag
        # print("Many1.to_yaml", repr(self))
        if isinstance(self.many1, str):
            return representer.represent_scalar(
                short_tag(cls._tag), self.many1)
        elif isinstance(self.many1, EbnfStr):
            return representer.represent_scalar(
                short_tag(cls._tag), self.many1.rule)
        elif isinstance(self.many1, EbnfBase):
            return representer.represent_scalar(
                short_tag(cls._tag), self.many1)
        elif isinstance(self.many1, (list, tuple)):
            return representer.represent_sequence(
                short_tag(cls._tag), self.many1)


@dataclass
class EbnfMap(EbnfBase):
    '''
    Instances of this class represent ISO 14977 SS 4.2 syntax-rules.

    The EBNF associated with syntax-rules is as follows

    .. code:: ebnf

       syntax =
           syntax rule, {syntax rule};
       syntax rule =
           meta identifier, '=',
           definitions list, ';';

    Syntax-rules can be represented in YAML as follows

    .. code:: yaml

       syntax:
         !many1 syntax rule
       syntax rule:
         - meta identifier
         - !token '='
         - definitions list
         - !token ';'
    '''
    rules: Dict[str, EbnfBase]
    _tag = 'tag:yaml.org,2002:map'
    # _tag = 'tag:drosoft.org/ebnf,2016:map'

    def __init__(self, rules):
        # from .schemas import EbnfMapSchema
        # EbnfMapSchema.validate(self._schema, rules)
        object.__init__(self)
        self.rules = rules

    def to_ebnf(self, converter):
        def to_str(s):
            if isinstance(s, EbnfStr):
                return str(s.rule)
            return str(s)
        converted = ['\n%s\n\t= %s;\n' %
                     (to_str(definiendum),
                      converter.convert(definiens))
                     for definiendum, definiens in self.rules.items()]
        return ''.join(converted)

    def to_lisp(self):
        from hy.models import Expression, Symbol
        # args = [self..to_lisp(),
        #         self.subtrahend.to_lisp()]
        return Expression(
            [Symbol("grammar")] +
            [
                # implicit EbnfMap
                [
                    # implicit EbnfAlt
                    Symbol(definiendum),
                    [
                        # implicit EbnfSeq
                        [
                            # explicit EbnfAlt is ok here
                            # explicit EbnfSeq is ok here
                            definiens.to_lisp()
                        ]
                        # implicit EbnfActions, NotImplemented
                    ]
                    # implicit alternatives
                ]
                for definiendum, definiens in self.rules.items()
            ])

    @classmethod
    def from_yaml(cls, constructor, node, deep=False):
        # print("EbnfMap", repr(node))
        # try:
        #     rules = OrderedDict([
        #         constructor.construct_mapping(node.value, deep=deep)])
        # except Exception:
        rules = OrderedDict([
            (definiendum.value,
             constructor.construct_object(definiens, deep=deep))
            for definiendum, definiens in node.value
        ])
        return cls(rules)

    @classmethod
    def to_yaml(cls, representer, self):
        return representer.represent_mapping(
            cls._tag, self.rules)


@dataclass
class EbnfMinus(EbnfBase):
    '''
    ISO 14977 SS 4.7 syntactic-exception
    '''
    minuend: EbnfBase
    subtrahend: EbnfBase
    _tag = 'tag:drosoft.org/ebnf,2016:minus'

    def __init__(self, minuend, subtrahend=None):
        object.__init__(self)
        if isinstance(minuend, list):
            if len(minuend) == 2:
                self.minuend = minuend[0]
                self.subtrahend = minuend[1]
            elif len(minuend) == 1:
                # TODO same as !not
                self.minuend = 'anychar'
                self.subtrahend = minuend[0]
            elif len(minuend) == 0:
                # TODO literally !anychar
                self.minuend = 'anychar'
                self.subtrahend = 'empty'
            else:
                raise ValueError
        else:
            self.minuend = minuend
            self.subtrahend = subtrahend

    def __iter__(self):
        yield self.minuend
        yield self.subtrahend

    def to_ebnf(self, parent):
        return '%s - %s' % (parent.convert(self.minuend),
                            parent.convert(self.subtrahend))

    def to_lisp(self):
        from hy.models import Expression, Symbol
        args = [self.minuend.to_lisp(),
                self.subtrahend.to_lisp()]
        return Expression(
            [Symbol("-")] + args)

    @classmethod
    def from_yaml(cls, constructor, node, deep=False):
        args = [constructor.construct_object(child, deep=deep)
                for child in node.value]
        return cls(*args)

    @classmethod
    def to_yaml(cls, representer, self):
        from .utils import short_tag
        return representer.represent_sequence(
            short_tag(cls._tag),
            [self.minuend,
             self.subtrahend])


@dataclass
class EbnfOpt(EbnfBase):
    '''
    '''
    opt: List[EbnfBase]
    lazy: bool
    _tag = 'tag:drosoft.org/ebnf,2016:opt'

    def __init__(self, opt, lazy=False):
        object.__init__(self)
        self.opt = opt
        self.lazy = lazy

    def __iter__(self):
        yield self.opt
        yield self.lazy

    def to_ebnf(self, parent):
        return '[ %s ]' % parent.convert(self.opt)

    def to_lisp(self):
        from hy.models import (Expression, Symbol)
        args = list(map(
            lambda self: self.to_lisp(),
            self.many))
        return Expression(
            [Symbol("?")] + args)

    @classmethod
    def from_yaml(cls, constructor, node, deep=False):
        if isinstance(node.value, str):
            return cls(opt=EbnfStr(node.value))
        elif isinstance(node.value, EbnfBase):
            return cls(opt=[node.value])
        elif isinstance(node.value, (list, tuple)):
            opt = [constructor.construct_object(child, deep=deep)
                   for child in node.value]
            return cls(opt=opt)

    @classmethod
    def to_yaml(cls, representer, self):
        from .utils import short_tag
        if isinstance(self.opt, str):
            return representer.represent_scalar(
                short_tag(cls._tag), self.opt)
        elif isinstance(self.opt, EbnfStr):
            return representer.represent_scalar(
                short_tag(cls._tag), self.opt.rule)
        elif isinstance(self.opt, EbnfBase):
            return representer.represent_sequence(
                short_tag(cls._tag), [self.opt])
        elif isinstance(self.opt, (list, tuple)):
            return representer.represent_sequence(
                short_tag(cls._tag), self.opt)


@dataclass
class EbnfRegExp(EbnfBase):
    '''
    '''
    regexp: str
    variant: str
    # variant="b" | basic
    # variant="e" | ext
    _tag = 'tag:drosoft.org/ebnf,2016:regexp'

    def __init__(self, regexp):
        object.__init__(self)
        self.regexp = regexp

    def __str__(self):
        return self.regexp

    def to_ebnf(self, parent):
        if not (self.regexp.startswith('/') and
                self.regexp.endswith('/')):
            self.regexp = '/' + self.regexp + '/'
        return '?%s?' % self.regexp

    def to_json(self):
        return {"regexp": self.regexp}

    @classmethod
    def from_yaml(cls, constructor, node, deep=False):
        return cls(regexp=str(node.value))

    @classmethod
    def to_yaml(cls, representer, self):
        from .utils import short_tag
        return representer.represent_scalar(
            short_tag(cls._tag), str(self.regexp))


@dataclass
class EbnfSepBy(EbnfBase):
    '''

    EbnfSepBy is not a fundamental structure. It can be represented as:

    .. code:: python

       EbnfSepBy(item=item, sepby=separator) ==
       EbnfSeq(
         seq=[
           item,
           EbnfMany(
             many=EbnfSeq(
               seq=[
                 separator,
                 item
               ]
             )
           )
         ]
       )

    So, for example, the grammar `element ( Comma element )*`
    can be written as `@sepEndBy[Comma element]`
    In Raku, this is written as `element % Comma`.
    '''
    sepby: EbnfBase
    item: EbnfBase
    _tag = 'tag:drosoft.org/ebnf,2016:sepby'

    def __init__(self, sepby, item):
        object.__init__(self)
        self.sepby = sepby
        self.item = item

    @classmethod
    def from_yaml(cls, constructor, node, deep=False):
        if isinstance(node.value, EbnfBase):
            raise ValueError
        elif isinstance(node.value, (list, tuple)):
            args = [constructor.construct_object(child, deep=deep)
                    for child in node.value]
            return cls(sepby=args[0],
                       item=args[1])

    @classmethod
    def to_yaml(cls, representer, self):
        from .utils import short_tag
        return representer.represent_sequence(
            short_tag(cls._tag),
            [self.item,
             self.sepby])


@dataclass
class EbnfSepEndBy(EbnfBase):
    '''
    '''
    sependby: EbnfBase
    item: EbnfBase
    _tag = 'tag:drosoft.org/ebnf,2016:sependby'

    def __init__(self, sependby, item):
        object.__init__(self)
        self.sependby = sependby
        self.item = item

    @classmethod
    def from_yaml(cls, constructor, node, deep=False):
        if isinstance(node.value, EbnfBase):
            raise ValueError
        elif isinstance(node.value, (list, tuple)):
            args = [constructor.construct_object(child, deep=deep)
                    for child in node.value]
            return cls(sependby=args[0],
                       item=args[1])

    @classmethod
    def to_yaml(cls, representer, self):
        from .utils import short_tag
        return representer.represent_sequence(
            short_tag(cls._tag),
            [self.item,
             self.sependby])


@dataclass
class EbnfSeq(EbnfBase):
    '''
    '''
    seq: List[EbnfBase]
    _tag = 'tag:yaml.org,2002:seq'
    # _tag = 'tag:drosoft.org/ebnf,2016:seq'

    def __init__(self, seq):
        object.__init__(self)
        assert isinstance(seq, list)
        self.seq = seq

    def __iter__(self):
        for item in self.seq:
            yield item

    def to_ebnf(self, converter):
        converted = ',\n\t'.join([
            converter.convert(value)
            for value in self.seq])
        if len(converted) < 80:
            converted = converted.replace('\n\t', ' ')
        return converted

    def to_lisp(self):
        from hy.models import Expression, Symbol
        args = list(map(
            lambda self: self.to_lisp(), self.seq))
        return Expression(
            [Symbol("seq")] + args)

    @classmethod
    def from_yaml(cls, constructor, node, deep=False):
        seq = [constructor.construct_object(child, deep=deep)
               for child in node.value]
        return cls(seq=seq)

    @classmethod
    def to_yaml(cls, representer, self):
        return representer.represent_sequence(
            cls._tag, self.seq)


@dataclass
class EbnfSpecial(EbnfBase):
    '''
    '''
    special: str
    _tag = 'tag:drosoft.org/ebnf,2016:special'

    def __init__(self, special):
        object.__init__(self)
        self.special = special

    def __str__(self):
        return self.special

    def to_ebnf(self, parent):
        return "? %s ?" % self.special

    def to_lisp(self):
        from hy.models import Expression, Symbol
        args = [self.special]
        return Expression(
            [Symbol("iso-ebnf-special")] + args)

    @classmethod
    def from_yaml(cls, constructor, node, deep=False):
        special = node.value
        return cls(special=special)

    @classmethod
    def to_yaml(cls, representer, self):
        from .utils import short_tag
        return representer.represent_scalar(
            short_tag(cls._tag),
            self.special)


@dataclass
class EbnfStr(EbnfBase):
    '''
    '''
    rule: str
    _tag = 'tag:yaml.org,2002:str'
    # _tag = 'tag:drosoft.org/ebnf,2016:rule'

    def __init__(self, rule):
        object.__init__(self)
        self.rule = rule

    def __str__(self):
        return self.rule

    def to_ebnf(self, parent):
        if isinstance(self.rule, (str, bytes)):
            return str(self.rule)
        return parent.convert(self.rule)

    def to_lisp(self):
        from hy.models import Symbol
        return Symbol(self.rule)

    def startswith(self, value):
        return self.rule.startswith(value)

    @classmethod
    def from_yaml(cls, constructor, node, deep=False):
        return cls(rule=node.value)

    @classmethod
    def to_yaml(cls, representer, self):
        # return representer.represent_str(self.rule)
        return representer.represent_data(self.rule)


@dataclass
class EbnfTimes(EbnfBase):
    '''
    '''
    times: EbnfBase
    minimum: int
    maximum: int
    lazy: bool
    _tag = 'tag:drosoft.org/ebnf,2016:times'

    def __init__(self, times, minimum=0, maximum=0, lazy=False):
        object.__init__(self)
        self.times = times
        self.minimum = minimum
        self.maximum = maximum
        self.lazy = lazy
        if isinstance(times, (list, tuple)):
            if len(times) > 3:
                self.lazy = times[3]
            if len(times) > 2:
                self.maximum = times[2]
            if len(times) > 1:
                self.minimum = times[1]
            if len(times) == 2:
                self.maximum = self.minimum
            if len(times) > 0:
                self.times = times[0]

        assert isinstance(minimum, int)
        assert isinstance(maximum, int)
        assert isinstance(lazy, bool)

    def __iter__(self):
        yield self.times
        yield self.minimum
        yield self.maximum
        yield self.lazy

    def to_ebnf(self, parent):
        if self.maximum == self.minimum:
            return '%d * %s' % (int(self.maximum),
                                parent.convert(self.times))
        else:
            raise ValueError("ISO EBNF does not support min/max repetition.")

    def to_lisp(self):
        from hy.models import (Expression, Symbol)
        args = [self.times.to_lisp()]
        if self.minimum == self.maximum:
            return Expression(
                [Symbol("="),
                 self.minimum] + args)
        else:
            return Expression(
                [Symbol("**"),
                 self.minimum,
                 self.maximum] + args)

    @classmethod
    def from_yaml(cls, constructor, node, deep=False):
        results = [constructor.construct_object(child)
                   for child in node.value]
        r = cls([])
        if len(results) == 4:
            r.times, r.minimum, r.maximum, r.lazy = results
        elif len(results) == 3:
            r.times, r.minimum, r.maximum = results
        elif len(results) == 2:
            r.times, r.minimum = results
            r.maximum = r.minimum
        elif len(results) == 1:
            r.times = results[0]
        else:
            raise ValueError
        return r

    @classmethod
    def to_yaml(cls, representer, self):
        from .utils import short_tag
        if self.minimum != self.maximum and \
           self.maximum != 0 and self.lazy:
            return representer.represent_sequence(
                short_tag(cls._tag),
                [self.times,
                 self.minimum,
                 self.maximum,
                 self.lazy])
        elif self.minimum != self.maximum and self.maximum != 0:
            return representer.represent_sequence(
                short_tag(cls._tag),
                [self.times,
                 self.minimum,
                 self.maximum])
        elif self.minimum == self.maximum and self.minimum != 0:
            return representer.represent_sequence(
                short_tag(cls._tag),
                [self.times,
                 self.minimum])
        else:
            return representer.represent_sequence(
                short_tag(cls._tag),
                [self.times])


@dataclass
class EbnfToken(EbnfBase):
    '''
      # This represents the characters matched.
      # For post-lexical-scanning productions,
      # You will have to make a new type.
      # Or you can use the grammar-parsing
      # production type, EbnfStr which
      # represents rule name references.
    '''
    token: str
    _tag = 'tag:drosoft.org/ebnf,2016:token'

    def __init__(self, token):
        object.__init__(self)
        self.token = token

    def __str__(self):
        return self.token

    def to_ebnf(self, _=None):
        if "'" in self.token:
            if '"' in self.token:
                return '"BAD:%s"' % self.token
            else:
                return '"%s"' % self.token
        else:
            return "'%s'" % self.token

    def to_lisp(self):
        return self.token

    @classmethod
    def from_yaml(cls, constructor, node, deep=False):
        return cls(token=node.value)

    @classmethod
    def to_yaml(cls, representer, self):
        from .utils import short_tag
        token = self.token
        if '\b' in token:
            token = repr(token)[1:-1].replace('x08', 't')
        if '\n' in token:
            token = repr(token)[1:-1]
        if '\r' in token:
            token = repr(token)[1:-1]
        return representer.represent_scalar(
            short_tag(cls._tag), token)
