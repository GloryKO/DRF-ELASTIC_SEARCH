from django.shortcuts import render

# Create your views here.
import abc
from django.http import HttpResponse
from elasticsearch_dsl import Q
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from blog.documents import *
from blog.serializers import *

class PaginatedElasticSearchView(APIView,LimitOffsetPagination): #class to be used by other classes
    serializer_class =None
    document_class =None

    @abc.abstractclassmethod
    def generate_q_expressions(self,query):

        """This method should be overridden
        and return a Q() expression."""

    def get(self,request,query):
        try: 
            q=self.generate_q_expressions(query) #get the query expression
            search = self.document_class.search().query(q) #perform search in the document
            response = search.execute() #execute search
            results=self.paginate_queryset(response,request,view=self) #paginate responses
            serializer = self.serializer_class(results) #serialize result
            return self.get_paginated_response(serializer.data) #return serialized data
        except Exception as e:
            return  HttpResponse(e,status=500)
    

class UserSearch(PaginatedElasticSearchView):
    serializer_class= UserSerializer
    document_class = UserDocument

    def generate_q_expression(self, query): #override the generate_q_expression in the superclass
        return Q("bool",
                 should=[
                     Q("match", username=query),
                     Q("match", first_name=query),
                     Q("match", last_name=query),
                 ], minimum_should_match=1)

class SearchCategories(PaginatedElasticSearchView):
    serializer_class = CategorySerializer
    document_class = CategoryDocument

    def generate_q_expression(self, query):
        return Q(
                "multi_match", query=query,
                fields=[
                    "name",
                    "description",
                ], fuzziness="auto")


class SearchArticles(PaginatedElasticSearchView):
    serializer_class = ArticleSerializer
    document_class = ArticleDocument

    def generate_q_expression(self, query):
        return Q(
                "multi_match", query=query,
                fields=[
                    "title",
                    "author",
                    "type",
                    "content"
                ], fuzziness="auto")