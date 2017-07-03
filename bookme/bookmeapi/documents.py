# http://elasticsearch-dsl.readthedocs.io/en/stable/search_dsl.html
# https://github.com/sabricot/django-elasticsearch-dsl
# https://github.com/elastic/elasticsearch-dsl-py/blob/master/docs/search_dsl.rst

from elasticsearch_dsl.connections import connections
from django_elasticsearch_dsl import DocType, Index
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

client = Elasticsearch()

my_search = Search(using=client)

from .models import Book

# Create a connection to ElasticSearch
connections.create_connection()

book = Index('books')

book.settings(
    number_of_shards=1,
    number_of_replicas=0
)


@book.doc_type
class BookDocument(DocType):

    class Meta:
        model = Book
        fields = ['title', 'isbn', 'category']


# define simple search here
# Simple search function
def search(title):
    query = my_search.query("match", title=title)
    response = query.execute()
    return response
