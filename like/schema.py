import graphene
from graphene_django import DjangoObjectType
from .models import Like

class LikeType(DjangoObjectType):
    class Meta:
        model = Like
        fields = "__all__"


class CreateLike(graphene.Mutation):
    class Arguments:
        content = graphene.ID(required=False)
        comment = graphene.ID(required=False)

    like = graphene.Field(LikeType)

    def mutate(self, info, content=None, comment=None):
        if not content and not comment:
            raise Exception("A Like needs to be related to a content or to a comment")
        if content and comment:
            raise Exception("A Like can either be related to content or comment")
        user = info.context.META["context"]["user"]
        like = Like(
            user=user,
            content=content,
            comment=comment
        )
        like.save()
        return CreateLike(like=like)


class DeleteLike(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            like = Like.objects.get(pk=id)
        except Like.DoesNotExist:
            raise Exception("Like not found")

        like.delete()
        return DeleteLike(success=True)


class Mutation(graphene.ObjectType):
    create_like = CreateLike.Field()
    delete_like = DeleteLike.Field()


schema = graphene.Schema(mutation=Mutation)