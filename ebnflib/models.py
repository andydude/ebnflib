import six
try:
    from collections.abc import Mapping, Sequence
except ImportError:
    from collections import Mapping, Sequence

from dataclasses import dataclass
EbnfBase = object


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
        if isinstance(obj, Sequence):
            return EbnfSeq(obj)
        elif isinstance(obj, six.string_types):
            return EbnfStr(obj)
        elif not isinstance(obj, Mapping):
            raise TypeError

        if 'alt' in obj:
            return EbnfAlt(**obj)
        elif 'between' in obj:
            return EbnfBetween(**obj)
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
    alt: list[EbnfBase]

    def __init__(self, alt):
        object.__init__(self)
        assert isinstance(alt, list)
        self.alt = alt

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

    @classmethod
    def from_yaml(cls, constructor, node, deep=False):
        alt = [constructor.construct_object(child, deep=deep)
               for child in node.value]
        return cls(alt=alt)

    @classmethod
    def to_yaml(cls, representer, self):
        from .utils import short_tag
        return representer.represent_sequence(short_tag(cls._tag), self.alt)


@dataclass
class EbnfBetween(EbnfBase):
    open: EbnfBase
    between: EbnfBase
    close: EbnfBase

    def __init__(self, open, close, between):
        object.__init__(self)
        self.open = open
        self.close = close
        self.between = between


@dataclass
class EbnfCharRange(EbnfBase):
    first: str
    last: str

    def __init__(self, first, last):
        object.__init__(self)
        assert isinstance(first, str)
        assert isinstance(last, str)
        self.first = first
        self.last = last


@dataclass
class EbnfCharSet(EbnfBase):
    chars: list[EbnfBase]
    negative: bool

    def __init__(self, chars, negative=False):
        object.__init__(self)
        assert isinstance(chars, list)
        self.chars = chars
        self.negative = negative


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

    def __init__(self, comment):
        object.__init__(self)
        self.comment = comment


@dataclass
class EbnfEmpty(EbnfBase):
    '''
    '''
    empty: type(None) = None

    def __init__(self, empty=None):
        object.__init__(self)
        self.empty = empty


@dataclass
class EbnfGroup(EbnfBase):
    '''
    '''
    group: EbnfBase

    def __init__(self, group):
        object.__init__(self)
        self.group = group

    def to_ebnf(self, parent):
        if isinstance(self.group, EbnfBase):
            inner = parent.convert(self.group)
            return '( %s )' % (inner)
        elif isinstance(self.group, (list, tuple)):
            inner = ' '.join(map(parent.convert, self.group))
            return '( %s )' % (inner)

    @classmethod
    def from_yaml(cls, constructor, node, deep=False):
        group = [constructor.construct_object(child, deep=deep)
                 for child in node.value]
        return cls(group=group)

    @classmethod
    def to_yaml(cls, representer, self):
        from .utils import short_tag
        if isinstance(self.group, EbnfBase):
            if isinstance(self.group, EbnfAlt):
                return type(self.group).to_yaml(representer, self.group)
            print("EbnfGroup.to_yaml.scalar", self.group)

            return representer.represent_scalar(
                short_tag(cls._tag), self.group)
        elif isinstance(self.group, (list, tuple)):
            print("EbnfGroup.to_yaml.sequence")
            return representer.represent_sequence(
                short_tag(cls._tag), self.group)


@dataclass
class EbnfMany(EbnfBase):
    '''
    '''
    many: EbnfBase
    lazy: bool

    def __init__(self, many, lazy=False):
        object.__init__(self)
        self.many = many
        self.lazy = lazy

    @classmethod
    def from_yaml(cls, constructor, node, deep=False):
        if isinstance(node.value, EbnfBase):
            return cls(many=node.value)
        elif isinstance(node.value, (list, tuple)):
            many = [constructor.construct_object(child, deep=deep)
                    for child in node.value]
            return cls(many=many)

    def to_ebnf(self, parent):
        converted = parent.convert(self.many)
        return "{ %s }" % converted

    @classmethod
    def to_yaml(cls, representer, self):
        from .utils import short_tag
        if isinstance(self.many, EbnfBase):
            return representer.represent_scalar(
                short_tag(cls._tag), self.many)
        elif isinstance(self.many, (list, tuple)):
            return representer.represent_sequence(
                short_tag(cls._tag), self.many)


@dataclass
class EbnfMany1(EbnfBase):
    '''
    '''
    many1: EbnfBase
    lazy: bool

    def __init__(self, many1, lazy=False):
        object.__init__(self)
        self.many1 = many1
        self.lazy = lazy

    @classmethod
    def from_yaml(cls, constructor, node, deep=False):
        if isinstance(node.value, EbnfBase):
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
        if isinstance(self.many1, EbnfBase):
            return representer.represent_scalar(
                short_tag(cls._tag), self.many1)
        elif isinstance(self.many1, (list, tuple)):
            return representer.represent_scalar(
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
    rules: dict[str, EbnfBase]

    def __init__(self, rules):
        from .schemas import EbnfMapSchema
        EbnfMapSchema.validate(self._schema, rules)
        object.__init__(self)
        self.rules = rules

    def to_ebnf(self, converter):
        converted = ['\n%s\n\t= %s;\n' %
                     (definiendum, converter.convert(definiens))
                     for definiendum, definiens in self.rules.items()]
        return ''.join(converted)


@dataclass
class EbnfMinus(EbnfBase):
    '''
    ISO 14977 SS 4.7 syntactic-exception
    '''

    def __init__(self, minuend, subtrahend):
        object.__init__(self)
        self.minuend = minuend
        self.subtrahend = subtrahend

    def to_ebnf(self, parent):
        return '%s - %s' % (parent.convert(self.minuend),
                            parent.convert(self.subtrahend))

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
    opt: EbnfBase
    lazy: bool

    def __init__(self, opt, lazy=False):
        object.__init__(self)
        self.opt = opt
        self.lazy = lazy

    def to_ebnf(self, parent):
        return '[ %s ]' % parent.convert(self.opt)

    @classmethod
    def from_yaml(cls, constructor, node, deep=False):
        if isinstance(node.value, EbnfBase):
            return cls(opt=node.value)
        elif isinstance(node.value, (list, tuple)):
            seq = [constructor.construct_object(child, deep=deep)
                   for child in node.value]
            return cls(opt=seq)

    @classmethod
    def to_yaml(cls, representer, self):
        from .utils import short_tag
        if isinstance(self.opt, EbnfBase):
            return representer.represent_scalar(
                short_tag(cls._tag), self.opt)
        elif isinstance(self.opt, (list, tuple)):
            return representer.represent_sequence(
                short_tag(cls._tag), self.opt)


@dataclass
class EbnfRegExp(EbnfBase):
    '''
    '''
    regexp: str

    def __init__(self, regexp):
        object.__init__(self)
        self.regexp = regexp

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
    item: EbnfBase
    sepby: EbnfBase

    def __init__(self, item, sepby):
        object.__init__(self)
        self.item = item
        self.sepby = sepby


@dataclass
class EbnfSepEndBy(EbnfBase):
    '''
    '''
    item: EbnfBase
    sependby: EbnfBase

    def __init__(self, item, sependby):
        object.__init__(self)
        self.item = item
        self.sependby = sependby


@dataclass
class EbnfSeq(EbnfBase):
    '''
    '''
    seq: list[EbnfBase]

    def __init__(self, seq):
        object.__init__(self)
        assert isinstance(seq, list)
        self.seq = seq

    def to_ebnf(self, converter):
        converted = ',\n\t'.join([
            converter.convert(value)
            for value in self.seq])
        if len(converted) < 80:
            converted = converted.replace('\n\t', ' ')
        return converted

    @classmethod
    def from_yaml(cls, constructor, node, deep=False):
        seq = [constructor.construct_object(child, deep=deep)
               for child in node.value]
        return cls(seq=seq)

    @classmethod
    def to_yaml(cls, representer, self):
        from .utils import short_tag
        return representer.represent_sequence(short_tag(cls._tag), self.seq)


@dataclass
class EbnfSpecial(EbnfBase):
    '''
    '''
    special: str

    def __init__(self, special):
        object.__init__(self)
        self.special = special

    def to_ebnf(self, parent):
        return "? %s ?" % self.special

    @classmethod
    def from_yaml(cls, constructor, node, deep=False):
        special = node.value
        return cls(special=special)

    @classmethod
    def to_yaml(cls, representer, self):
        from .utils import short_tag
        return representer.represent_scalar(short_tag(cls._tag), self.special)


@dataclass
class EbnfStr(EbnfBase):
    '''
    '''
    rule: str

    def __init__(self, rule):
        object.__init__(self)
        self.rule = rule

    def __repr__(self):
        return '%s(rule=%s)' % (
            type(self).__name__,
            repr(self.rule))

    def to_ebnf(self, parent):
        if isinstance(self.rule, (str, bytes)):
            return str(self.rule)
        return parent.convert(self.rule)

    def startswith(self, value):
        return self.rule.startswith(value)


@dataclass
class EbnfTimes(EbnfBase):
    '''
    '''
    times: EbnfBase
    minimum: int
    maximum: int

    def __init__(self, times, maximum=None, minimum=None):
        object.__init__(self)
        self.maximum = maximum
        self.minimum = minimum
        self.times = times

    def to_ebnf(self, parent):
        if self.maximum == self.minimum:
            return '%d * %s' % (int(self.maximum),
                                parent.convert(self.times))
        else:
            raise ValueError("ISO EBNF does not support min/max repetition.")

    @classmethod
    def from_yaml(cls, constructor, node, deep=False):
        results = [constructor.construct_object(child)
                   for child in node.value]
        r = cls(None)
        if len(results) == 3:
            r.minimum, r.maximum, r.times = results
        elif len(results) == 2:
            r.maximum, r.times = results
            r.minimum = r.maximum
        elif len(results) == 1:
            r.times = results
        else:
            raise ValueError
        return r

    @classmethod
    def to_yaml(cls, representer, self):
        from .utils import short_tag
        if isinstance(self.times, EbnfBase):
            return representer.represent_scalar(
                short_tag(cls._tag), self.times)
        elif isinstance(self.times, (list, tuple)):
            return representer.represent_sequence(
                short_tag(cls._tag), self.times)


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

    def __init__(self, token):
        object.__init__(self)
        self.token = token

    def to_ebnf(self, _=None):
        if "'" in self.token:
            if '"' in self.token:
                return '"BAD:%s"' % self.token
            else:
                return '"%s"' % self.token
        else:
            return "'%s'" % self.token

    @classmethod
    def from_yaml(cls, constructor, node, deep=False):
        return cls(token=node.value)

    @classmethod
    def to_yaml(cls, representer, self):
        from .utils import short_tag
        return representer.represent_scalar(
            short_tag(cls._tag), str(self.token))
