import graphene
from graphene_django import DjangoObjectType
from django.db.models import Q
from .models import User

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "emoji_unicode")

class Query(graphene.ObjectType):
    users = graphene.List(UserType, name=graphene.String(), last=graphene.Int(), offset=graphene.Int())

    def resolve_users(self, info, name=None, last=10, offset=0):
        """
        The resolve_users function is a resolver. It's responsible for retrieving the users from the database and returning them to GraphQL.

        :param self: Refer to the current instance of a class
        :param info: Pass along the context of the query
        :return: All user objects from the database
        """
        if name:
            return User.objects.all().filter(Q(first_name__contains=name) | Q(last_name__contains=name))[offset:offset+last]
        return User.objects.all()[offset:offset+last]


schema = graphene.Schema(query=Query)