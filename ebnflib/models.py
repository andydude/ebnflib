from collections import Mapping, Sequence
import six


class EbnfAny(object):
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


class EbnfAlt(object):
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
        alt = [constructor.construct_object(child, deep=deep) for child in node.value]
        return cls(alt=alt)

    @classmethod
    def to_yaml(cls, representer, self):
        from .utils import short_tag
        return representer.represent_sequence(short_tag(cls._tag), self.alt)


class EbnfComment(object):
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

    def __init__(self, comment):
        object.__init__(self)
        self.comment = comment


class EbnfEmpty(object):
    '''
    '''

    def __init__(self, empty):
        object.__init__(self)
        self.empty = empty


class EbnfGroup(object):
    '''
    '''

    def __init__(self, group):
        object.__init__(self)
        self.group = group

    def to_ebnf(self, parent):
        inner = ' '.join(map(parent.convert, self.group))
        return '( %s )' % (inner)

    @classmethod
    def from_yaml(cls, constructor, node, deep=False):
        group = [constructor.construct_object(child, deep=deep) for child in node.value]
        return cls(group=group)

    @classmethod
    def to_yaml(cls, representer, self):
        from .utils import short_tag
        return representer.represent_sequence(
            short_tag(cls._tag), self.group)


class EbnfMany(object):
    '''
    '''

    def __init__(self, many):
        object.__init__(self)
        self.many = many

    @classmethod
    def from_yaml(cls, constructor, node, deep=False):
        if isinstance(node.value, (list, tuple)):
            many = [constructor.construct_object(child, deep=deep) for child in node.value]
            return cls(many=many)
        else:
            return cls(many=node.value)
        
    def to_ebnf(self, parent):
        converted = parent.convert(self.many)
        return "{ %s }" % converted

    @classmethod
    def to_yaml(cls, representer, self):
        from .utils import short_tag
        if isinstance(self.many, (list, tuple)):
            return representer.represent_sequence(
                short_tag(cls._tag), self.many)
        else:
            return representer.represent_scalar(
                short_tag(cls._tag), self.many)


class EbnfMany1(object):
    '''
    '''

    def __init__(self, many1):
        object.__init__(self)
        self.many1 = many1

    @classmethod
    def from_yaml(cls, constructor, node, deep=False):
        if isinstance(node.value, (list, tuple)):
            many1 = [constructor.construct_object(child, deep=deep) for child in node.value]
            return cls(many1=many1)
        else:
            return cls(many1=node.value)

    def to_ebnf(self, parent):
        converted = parent.convert(self.many1)
        return "%s, { %s }" % (converted, converted)

    @classmethod
    def to_yaml(cls, representer, self):
        from .utils import short_tag
        if isinstance(self.many1, (list, tuple)):
            return representer.represent_scalar(
                short_tag(cls._tag), self.many1)
        else:
            return representer.represent_scalar(
                short_tag(cls._tag), self.many1)


class EbnfMap(object):
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

class EbnfMinus(object):
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


class EbnfOpt(object):
    '''
    '''

    def __init__(self, opt):
        object.__init__(self)
        self.opt = opt

    def to_ebnf(self, parent):
        return '[ %s ]' % parent.convert(self.opt)

    @classmethod
    def from_yaml(cls, constructor, node, deep=False):
        if isinstance(node.value, (list, tuple)):
            return constructor.construct_object(node.value)
        else:
            return cls(opt=node.value)

    @classmethod
    def to_yaml(cls, representer, self):
        from .utils import short_tag
        if isinstance(self.opt, (list, tuple)):
            return representer.represent_sequence(
                short_tag(cls._tag), self.opt)
        else:
            return representer.represent_scalar(
                short_tag(cls._tag), self.opt)


class EbnfRegExp(object):
    '''
    '''

    def __init__(self, regexp):
        object.__init__(self)
        self.regexp = regexp

    def to_ebnf(self, parent):
        if not (self.regexp.startswith('/') and \
                self.regexp.endswith('/')):
            self.regexp = '/' + self.regexp + '/'
        return '?%s?' % self.regexp

    def to_json(self):
        return {"regexp": self.regexp}

    @classmethod
    def from_yaml(cls, constructor, node, deep=False):
        return cls(regexp=unicode(node.value))

    @classmethod
    def to_yaml(cls, representer, self):
        from .utils import short_tag
        return representer.represent_scalar(
            short_tag(cls._tag), unicode(self.regexp))


class EbnfSeq(object):
    '''
    '''

    def __init__(self, seq):
        object.__init__(self)
        assert isinstance(seq, list)
        self.seq = seq

    def to_ebnf(self, converter):
        converted = ',\n\t'.join([converter.convert(value)
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


class EbnfSpecial(object):
    '''
    '''

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


class EbnfStr(object):
    '''
    '''

    def __init__(self, rule):
        object.__init__(self)
        self.rule = rule

    def __repr__(self):
        return '%s(rule=%s)' % (
            type(self).__name__,
            repr(self.rule))
    
    def to_ebnf(self, parent):
        if isinstance(self.rule, (str, unicode)):
            return unicode(self.rule)
        return parent.convert(self.rule)

    def startswith(self, value):
        return self.rule.startswith(value)


class EbnfTimes(object):
    '''
    '''

    def __init__(self, times, maximum=None, minimum=None):
        object.__init__(self)
        self.maximum = maximum
        self.minimum = minimum
        self.times = times

    def to_ebnf(self, parent):
        return '%d * %s' % (int(self.args[0]),
                            parent.convert(self.args[1]))

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
        if isinstance(self.times, (list, tuple)):
            return representer.represent_sequence(
                short_tag(cls._tag), self.times)
        else:
            return representer.represent_scalar(
                short_tag(cls._tag), self.times)


class EbnfToken(object):
    '''
    '''

    def __init__(self, token):
        object.__init__(self)
        self.token = token

    def to_ebnf(self, _=None):
        if "'" in self.token:
            if '"' in self.token:
                raise ValueError
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
            short_tag(cls._tag), unicode(self.token))
