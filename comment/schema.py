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
        content = graphene.ID(required=True)
        body = graphene.String(required=True)

    comment = graphene.Field(CommentType)

    def mutate(self, info, content, body):
        """
        The mutate function is the function that will be called when a client
        makes a request to this mutation. It takes in four arguments:
        self, info, title and comment. The first two are required by all mutations;
        the last two are the arguments we defined in our CreateCommentInput class.

        :param self: Access the object's attributes and methods
        :param info: Access the context of the request
        :param title: Create a new comment with the title provided
        :param comment: Pass the comment of the comment
        :param author_id: Get the author object from the database
        :return: A createcomment object
        """
        user = info.context.META["context"]["user"]
        content = Content.objects.get(id=content)
        comment = Comment(
            owner=user,
            content=content,
            body=body
        )
        comment.save()
        return CreateComment(comment=comment)


class UpdateComment(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        body = graphene.String()

    comment = graphene.Field(CommentType)

    def mutate(self, info, id, body=None):
        """
        The mutate function is the function that will be called when a client
        calls this mutation. It takes in four arguments: self, info, id and title.
        The first two are required by all mutations and the last two are specific to this mutation.
        The self argument refers to the class itself (UpdateComment) while info contains information about
        the query context such as authentication credentials or access control lists.

        :param self: Pass the instance of the class
        :param info: Access the context of the request
        :param id: Find the comment we want to update
        :param title: Update the title of a comment
        :param comment: Update the comment of a comment
        :return: An instance of the updatecomment class, which is a subclass of mutation
        """
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
        """
        The mutate function is the function that will be called when a client
        calls this mutation. It takes in four arguments: self, info, id. The first
        argument is the object itself (the class instance). The second argument is
        information about the query context and user making this request. We don't
        need to use it here so we'll just pass it along as-is to our model method.
        The third argument is an ID of a comment we want to delete.

        :param self: Represent the instance of the class
        :param info: Access the context of the query
        :param id: Find the comment that is to be deleted
        :return: A deletecomment object, which is the return type of the mutation
        """
        try:
            comment = Comment.objects.get(pk=id)
        except Comment.DoesNotExist:
            raise Exception("Comment not found")

        comment.delete()
        return DeleteComment(success=True)


class Query(graphene.ObjectType):
    comments = graphene.List(CommentType, content_id=graphene.ID(), last=graphene.Int(), offset=graphene.Int())

    def resolve_comments(self, info, content_id, last=10, offset=0):
        """
        The resolve_comments function is a resolver. It's responsible for retrieving
        the comments under a content from the database and returning them to GraphQL.

        :param self: Refers to the current instance of a class
        :param info: Pass along the context of the query
        :param last: Refers to the count of last records needs to be returned
        :param offset: Refers to the count of how many records has already been returned
        :return: Last records starting from offset to last from the database
        """
        return Comment.objects.all().filter(content=content_id)\
                .order_by('-created_at')[offset:offset+last]


class Mutation(graphene.ObjectType):
    create_comment = CreateComment.Field()
    update_comment = UpdateComment.Field()
    delete_comment = DeleteComment.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)