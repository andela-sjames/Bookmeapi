# source: https://github.com/graphql-python/graphene-django/
# https://facebook.github.io/relay/graphql/mutations.htm
# https://facebook.github.io/relay/graphql/mutations.htm
# http://docs.graphene-python.org/projects/django/en/latest/tutorial-plain/

import graphene
from graphene import relay, ObjectType, InputObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from django.contrib.auth.models import User

class UserCreateInput(InputObjectType):
    username = graphene.String(required=True)
    first_name = graphene.String(required=False)
    last_name = graphene.String(required=False)
    email = graphene.String(required=True)
    is_staff = graphene.Boolean(required=False)
    is_active = graphene.Boolean(required=False)
    password = graphene.String(required=True)


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

        return CreateUser(new_user=new_user)


class Query(ObjectType):
    users = relay.Node.Field(UserNode) # get user by id or by field name
    all_users =  DjangoFilterConnectionField(UserNode) # get all users

    def resolve_users(self):
        return User.objects.all()


class Mutation(ObjectType):
     create_user = CreateUser.Field()
    

schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
)
