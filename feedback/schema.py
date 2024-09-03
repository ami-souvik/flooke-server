import graphene
from graphene_django import DjangoObjectType
from .models import Feedback
from content.models import Content
from comment.models import Comment

class FeedbackType(DjangoObjectType):
    class Meta:
        model = Feedback
        fields = "__all__"


class CreateFeedback(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        what = graphene.String(required=True)
        vote = graphene.String(required=True) #upvote or downvote

    feedback = graphene.Field(FeedbackType)

    def mutate(self, info, id, what, vote):
        if what != "comment" and what != "content":
            raise Exception("A Feedback needs to be related to a content or to a comment")
        if vote != "U" and vote != "D":
            raise Exception("A Feedback can only be of type upvote or downvote")
        user = info.context.META["context"]["user"]
        content = None
        comment = None
        if what == "content":
            content=Content.objects.get(id=id)
        if what == "comment":
            comment=Comment.objects.get(id=id)
        feedback = Feedback.objects.filter(
            user=user,
            content=content,
            comment=comment
        ).first()
        if not feedback:
            feedback = Feedback(
                user=user,
                content=content,
                comment=comment
            )
        feedback.vote = vote
        feedback.save()
        return CreateFeedback(feedback=feedback)


class DeleteFeedback(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            feedback = Feedback.objects.get(pk=id)
        except Feedback.DoesNotExist:
            raise Exception("Feedback not found")

        feedback.delete()
        return DeleteFeedback(success=True)


class Query(graphene.ObjectType):
    feedbacks = graphene.List(FeedbackType, content=graphene.ID(), last=graphene.Int(), offset=graphene.Int())

    def resolve_feedbacks(self, info, content, last=10, offset=0):
        return Feedback.objects.filter(content=content)\
                .order_by('-created_at')[offset:offset+last]


class Mutation(graphene.ObjectType):
    create_feedback = CreateFeedback.Field()
    delete_feedback = DeleteFeedback.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)