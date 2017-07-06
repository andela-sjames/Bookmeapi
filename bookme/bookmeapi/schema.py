# source: https://github.com/graphql-python/graphene-django/
# https://facebook.github.io/relay/graphql/mutations.htm
# https://facebook.github.io/relay/graphql/mutations.htm
# http://docs.graphene-python.org/projects/django/en/latest/tutorial-plain/

import graphene
from graphene import relay, ObjectType, InputObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField


from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from bookmeapi.models import Book, Issue
from bookmeapi.helpers import get_object, get_errors, update_create_instance


class UserCreateInput(InputObjectType):
    username = graphene.String(required=True)
    first_name = graphene.String(required=False)
    last_name = graphene.String(required=False)
    email = graphene.String(required=True)
    is_staff = graphene.Boolean(required=False)
    is_active = graphene.Boolean(required=False)
    password = graphene.String(required=True)

class BookCreateInput(InputObjectType):
    title = graphene.String(required=False)
    isbn = graphene.String(required=False)
    category = graphene.String(required=False)


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        # Allow for some more advanced filtering here
        filter_fields = {
            'first_name': ['exact', 'icontains', 'istartswith'],
            'last_name': ['exact', 'icontains', 'istartswith'],
            'username': ['exact'],
        }
        interfaces = (relay.Node, )


class BookNode(DjangoObjectType):
    class Meta:
        model = Book
        filter_fields = {
            'title': ['exact','istartswith'],
            'isbn':['exact'],
            'category':['exact', 'icontains','istartswith'],
        }
        interfaces = (relay.Node, )

class CreateUser(relay.ClientIDMutation):

    class Input:
         user = graphene.Argument(UserCreateInput)

    new_user = graphene.Field(UserNode)

    @classmethod
    def mutate_and_get_payload(cls, args, context, info):

        user_data = args.get('user')
        # unpack the dict item into the model instance
        new_user = User.objects.create(**user_data)
        new_user.set_password(user_data.get('password'))
        new_user.save()

        return cls(new_user=new_user)


class CreateBook(relay.ClientIDMutation):
    
    class Input:
         book = graphene.Argument(BookCreateInput)

    new_book = graphene.Field(BookNode)

    @classmethod
    def mutate_and_get_payload(cls, args, context, info):

        book_data = args.get('book')
        book = Book()
        new_book = update_create_instance(book, book_data)

        return cls(new_book=new_book)


class UpdateBook(relay.ClientIDMutation):

    class Input:
        book = graphene.Argument(BookCreateInput)
        id = graphene.String(required=True)

    errors = graphene.List(graphene.String)
    updated_book = graphene.Field(BookNode)

    @classmethod
    def mutate_and_get_payload(cls, args, context, info):

        try:
            book_instance = get_object(Book, args['id'])
            if book_instance:
                book_data = args.get('book')
                updated_book = update_create_instance(book_instance, book_data)
            return cls(updated_book=updated_book)
        except ValidationError as e:
            return cls(updated_book=None, errors=get_errors(e))


class Query(ObjectType):
    users = relay.Node.Field(UserNode) # get user by id or by field name
    all_users =  DjangoFilterConnectionField(UserNode) # get all users
    books = relay.Node.Field(BookNode)
    all_books = DjangoFilterConnectionField(BookNode)

    def resolve_users(self):
        return User.objects.all()
    
    def resolve_books(self):
        return Book.objects.all()    


class Mutation(ObjectType):
     create_user = CreateUser.Field()
     create_book = CreateBook.Field()
     update_book = UpdateBook.Field()
    

schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
)
