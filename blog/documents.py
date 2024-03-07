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

