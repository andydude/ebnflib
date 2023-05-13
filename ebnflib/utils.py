import os.path
import yaml
import weakref

def init_crossrefs():
    from ebnflib import models, schemas
    
    models_schema = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'models.schema.yaml')
    
    with open(models_schema) as reader:
        data = yaml.safe_load(reader.read())

    for definiendum, definiens in data['definitions'].items():
        schema = getattr(schemas, definiendum + 'Schema')
        model = getattr(models, definiendum)

        schema.__model_class = weakref.ref(model)
        model._schema = schema()

        if 'required' in definiens:
            model._required = definiens['required']
            
        if 'x-tag' in definiens:
            model._tag = definiens['x-tag']

        # print(model)
        # print(schema)

def short_tag(long_tag):
    return '!' + long_tag.rsplit(':', 1)[1]
