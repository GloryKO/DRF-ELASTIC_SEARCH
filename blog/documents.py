from django.contrib.auth.models import User
from django_elasticsearch_dsl import Document,fields
from django_elasticsearch_dsl.registries import registry
from .models import *

@registry.register_document #creates and register a user document
class UserDocument(Document):
    class Index:
        name ="users"
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }
    class Django:
        model =User
        fields=["id","first_name","last_name","username"]

@registry.register_document
class CategoryDocument(Document):
    id =fields.IntegerField()
    class Index:
        name="categories"
        settings ={
            "number_of_shards":1,
            "number_of_replicas":0,
        }
    class Django:
        model =Category
        fields = ["name","description",]
    
@registry.register_document
class ArticleDocument(Document): #define the foreign keys (author and categories)
    author = fields.ObjectField(properties={
        "id":fields.IntegerField(),
        "first_name":fields.TextField(),
        "last_name":fields.TextField(),
        "user_name":fields.TextField(),

    })
    categories = fields.ObjectField(properties={
        "id":fields.IntegerField(),
        "name":fields.TextField(),
        "description":fields.TextField()
    })
    type = fields.TextField(attr="type_to_string")
    class Index:
        name ="aticle"
        settings ={
            "number_of_shards":1,
            "number_of_replica":0,
        }
    class Django:
        model = Article
        fields=[ "title",
            "content",
            "created_datetime",
            "updated_datetime"
            ]
