from marshmallow import Schema, fields

class EbnfAnySchema(Schema):
    '''
    '''
    pass

class EbnfAltSchema(Schema):
    '''
    '''
    alt = fields.Nested(EbnfAnySchema, many=True)

class EbnfCommentSchema(Schema):
    '''
    '''
    comment = fields.Nested(EbnfAnySchema)

class EbnfEmptySchema(Schema):
    '''
    '''
    empty = fields.String()

class EbnfGroupSchema(Schema):
    '''
    '''
    group = fields.Nested(EbnfAnySchema)

class EbnfManySchema(Schema):
    '''
    '''
    many = fields.Nested(EbnfAnySchema)

class EbnfMany1Schema(Schema):
    '''
    '''
    many1 = fields.Nested(EbnfAnySchema)

class EbnfMapSchema(Schema):
    '''
    '''
    rules = fields.Nested(EbnfAnySchema)

class EbnfMinusSchema(Schema):
    '''
    '''
    minuend = fields.Nested(EbnfAnySchema)
    subtrahend = fields.Nested(EbnfAnySchema)

class EbnfOptSchema(Schema):
    '''
    '''
    opt = fields.Nested(EbnfAnySchema)

class EbnfRegExpSchema(Schema):
    '''
    '''
    regexp = fields.String()

class EbnfSeqSchema(Schema):
    '''
    '''
    seq = fields.Nested(EbnfAnySchema, many=True)

class EbnfSpecialSchema(Schema):
    '''
    '''
    special = fields.Nested(EbnfAnySchema)

class EbnfStrSchema(Schema):
    '''
    '''
    rule = fields.String()

class EbnfTimesSchema(Schema):
    '''
    '''
    maximum = fields.Integer()
    minimum = fields.Integer()
    times = fields.Nested(EbnfAnySchema)

class EbnfTokenSchema(Schema):
    '''
    '''
    token = fields.String()
