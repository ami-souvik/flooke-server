import graphene
from graphene_django import DjangoObjectType
from django.db.models import Q
from basic_auth.models import User

class CurrentUserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "emoji_unicode")


class UpdateCurrent(graphene.Mutation):
    class Arguments:
        emoji_unicode = graphene.String()
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()

    current = graphene.Field(CurrentUserType)

    def mutate(self, info, emoji_unicode=None, first_name=None, last_name=None, email=None):
        try:
            user = info.context.META["context"]["user"]
            current = User.objects.get(id=user.id)
        except User.DoesNotExist:
            raise Exception("User not found")

        if emoji_unicode is not None:
            current.emoji_unicode = emoji_unicode

        if first_name is not None:
            current.first_name = first_name

        if last_name is not None:
            current.last_name = last_name

        if email is not None:
            current.email = email

        current.save()
        return UpdateCurrent(current=current)


class Query(graphene.ObjectType):
    current = graphene.Field(CurrentUserType)

    def resolve_current(self, info):
        """
        The resolve_current_users function is a resolver. It's responsible for retrieving the current
        authenticated user detailss from the database and returning them to GraphQL.

        :param self: Refer to the current instance of a class
        :param info: Pass along the context of the query
        :return: The current authenticated user object from the database
        """
        user = info.context.META["context"]["user"]
        return User.objects.get(id=user.id)


class Mutation(graphene.ObjectType):
    update_current = UpdateCurrent.Field()

schema = graphene.Schema(query=Query)