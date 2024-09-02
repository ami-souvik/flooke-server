import graphene
from graphene_django import DjangoObjectType
from .models import Comment
from content.models import Content

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = "__all__"


class CreateComment(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        what = graphene.ID(required=True)
        body = graphene.String(required=True)

    comment = graphene.Field(CommentType)

    def mutate(self, info, id, what, body):
        if what != "comment" and what != "content" :
            raise Exception("A Comment needs to be related to a content or to a comment")

        user = info.context.META["context"]["user"]
        content = None
        comment = None
        if what == "content":
            content=Content.objects.get(id=id)
        if what == "comment":
            comment=Comment.objects.get(id=id)

        comment = Comment(
            owner=user,
            content=content,
            comment=comment,
            body=body
        )
        comment.save()
        return CreateComment(comment=comment)


class UpdateComment(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        body = graphene.String(required=True)

    comment = graphene.Field(CommentType)

    def mutate(self, info, id, body=None):
        try:
            comment = Comment.objects.get(pk=id)
        except Comment.DoesNotExist:
            raise Exception("Comment not found")

        if body is not None:
            comment.body = body

        comment.save()
        return UpdateComment(comment=comment)


class DeleteComment(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            comment = Comment.objects.get(pk=id)
        except Comment.DoesNotExist:
            raise Exception("Comment not found")

        comment.delete()
        return DeleteComment(success=True)


class Query(graphene.ObjectType):
    comments = graphene.List(CommentType, content=graphene.ID(), last=graphene.Int(), offset=graphene.Int())

    def resolve_comments(self, info, content, last=10, offset=0):
        """
        The resolve_comments function is a resolver. It's responsible for retrieving
        the comments under a content from the database and returning them to GraphQL.

        :param self: Refers to the current instance of a class
        :param info: Pass along the context of the query
        :param last: Refers to the count of last records needs to be returned
        :param offset: Refers to the count of how many records has already been returned
        :return: Last records starting from offset to last from the database
        """
        return Comment.objects.filter(content=content)\
                .order_by('-created_at')[offset:offset+last]


class Mutation(graphene.ObjectType):
    create_comment = CreateComment.Field()
    update_comment = UpdateComment.Field()
    delete_comment = DeleteComment.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)