import graphene
from graphene_django import DjangoObjectType, DjangoListField
from .models import Comment
from content.models import Content
from feedback.models import Feedback
from feedback.schema import FeedbackType

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = "__all__"

    upvote_count = graphene.Int()

    @staticmethod
    def resolve_upvote_count(self, info):
        return self.feedbacks.filter(vote="U").count()

    downvote_count = graphene.Int()

    @staticmethod
    def resolve_downvote_count(self, info):
        return self.feedbacks.filter(vote="D").count()

    feedback = graphene.Field(FeedbackType)
    
    @staticmethod
    def resolve_feedback(self, info):
        user = info.context.META["context"]["user"]
        return Feedback.objects.filter(user=user, comment=self).first()

    feedbacks = DjangoListField(FeedbackType, last=graphene.Int(), offset=graphene.Int())

    @staticmethod
    def resolve_feedbacks(self, info, last=10, offset=0):
        return self.feedbacks.order_by('-created_at')[offset:offset+last]
    
    comment_count = graphene.Int()

    @staticmethod
    def resolve_comment_count(self, info):
        return self.comments.count()

    comments = DjangoListField(lambda: CommentType, last=graphene.Int(), offset=graphene.Int())

    @staticmethod
    def resolve_comments(self, info, last=10, offset=0):
        return self.comments.order_by('-created_at')[offset:offset+last]


class CreateComment(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        what = graphene.String(required=True)
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
            comment.has_reply = True
            comment.save()

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
            if comment.comment:
                comment.comment.has_reply = False
                comment.comment.save()
        except Comment.DoesNotExist:
            raise Exception("Comment not found")

        comment.delete()
        return DeleteComment(success=True)


class Query(graphene.ObjectType):
    comments = graphene.List(CommentType, id=graphene.ID(required=True), what=graphene.String(required=True),
                             last=graphene.Int(), offset=graphene.Int())

    def resolve_comments(self, info, id, what, last=10, offset=0):
        if what == "content":
            return Comment.objects.filter(content=id)\
                .order_by('-created_at')[offset:offset+last]
        if what == "comment":
            return Comment.objects.filter(comment=id)\
                .order_by('-created_at')[offset:offset+last]
        raise Exception("A Comment needs to be related to a content or to a comment")


class Mutation(graphene.ObjectType):
    create_comment = CreateComment.Field()
    update_comment = UpdateComment.Field()
    delete_comment = DeleteComment.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)