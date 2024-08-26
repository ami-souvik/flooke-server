import graphene
from graphene_django import DjangoObjectType
from .models import User

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "emoji_unicode")

class Query(graphene.ObjectType):
    users = graphene.List(UserType)

    def resolve_users(self, info):
        """
        The resolve_users function is a resolver. It's responsible for retrieving the users from the database and returning them to GraphQL.

        :param self: Refer to the current instance of a class
        :param info: Pass along the context of the query
        :return: All user objects from the database
        """
        return User.objects.all()


schema = graphene.Schema(query=Query)