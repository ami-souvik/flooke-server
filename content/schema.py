import graphene
from graphene_django import DjangoObjectType, DjangoListField
from .models import Content
from comment.schema import CommentType
from comment.models import Comment
from feedback.schema import FeedbackType
from feedback.models import Feedback

class ContentType(DjangoObjectType):
    class Meta:
        model = Content
        fields = "__all__"

    feedback = graphene.Field(FeedbackType)
    
    @staticmethod
    def resolve_feedback(self, info):
        user = info.context.user
        return Feedback.objects.filter(user=user, content=self).first()

    comment_count = graphene.Int()

    @staticmethod
    def resolve_comment_count(self, info):
        return self.comments.count()

    comments = DjangoListField(CommentType, comment=graphene.ID(), last=graphene.Int(), offset=graphene.Int())

    @staticmethod
    def resolve_comments(self, info, comment, last=10, offset=0):
        try:
            comment = Comment.objects.get(id=comment)
            return [comment]
        except Comment.DoesNotExist:
            return self.comments.order_by('-created_at')[offset:offset+last]

    upvote_count = graphene.Int()

    @staticmethod
    def resolve_upvote_count(self, info):
        return self.feedbacks.filter(vote="U").count()

    downvote_count = graphene.Int()

    @staticmethod
    def resolve_downvote_count(self, info):
        return self.feedbacks.filter(vote="D").count()

    feedbacks = DjangoListField(FeedbackType, last=graphene.Int(), offset=graphene.Int())

    @staticmethod
    def resolve_feedbacks(self, info, last=10, offset=0):
        return self.feedbacks.order_by('-created_at')[offset:offset+last]

class CreateContent(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        body = graphene.String(required=True)

    content = graphene.Field(ContentType)

    def mutate(self, info, title, body):
        """
        The mutate function is the function that will be called when a client
        makes a request to this mutation. It takes in four arguments:
        self, info, title and content. The first two are required by all mutations;
        the last two are the arguments we defined in our CreateContentInput class.

        :param self: Access the object's attributes and methods
        :param info: Access the context of the request
        :param title: Create a new content with the title provided
        :param content: Pass the content of the content
        :param author_id: Get the author object from the database
        :return: A createcontent object
        """
        user = info.context.user
        content = Content(
            owner=user,
            title=title,
            body=body
        )
        content.save()
        return CreateContent(content=content)


class UpdateContent(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        body = graphene.String()

    content = graphene.Field(ContentType)

    def mutate(self, info, id, title=None, body=None):
        """
        The mutate function is the function that will be called when a client
        calls this mutation. It takes in four arguments: self, info, id and title.
        The first two are required by all mutations and the last two are specific to this mutation.
        The self argument refers to the class itself (UpdateContent) while info contains information about
        the query context such as authentication credentials or access control lists.

        :param self: Pass the instance of the class
        :param info: Access the context of the request
        :param id: Find the content we want to update
        :param title: Update the title of a content
        :param content: Update the content of a content
        :return: An instance of the updatecontent class, which is a subclass of mutation
        """
        try:
            content = Content.objects.get(pk=id)
        except Content.DoesNotExist:
            raise Exception("Content not found")

        if title is not None:
            content.title = title
        if body is not None:
            content.body = body

        content.save()
        return UpdateContent(content=content)


class DeleteContent(graphene.Mutation):
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
        The third argument is an ID of a content we want to delete.

        :param self: Represent the instance of the class
        :param info: Access the context of the query
        :param id: Find the content that is to be deleted
        :return: A deletecontent object, which is the return type of the mutation
        """
        try:
            content = Content.objects.get(pk=id)
        except Content.DoesNotExist:
            raise Exception("Content not found")

        content.delete()
        return DeleteContent(success=True)


class Query(graphene.ObjectType):
    contents = graphene.List(ContentType, content=graphene.ID(), last=graphene.Int(), offset=graphene.Int())
    
    def resolve_contents(self, info, content=None, last=10, offset=0):
        """
        The resolve_contents function is a resolver. It's responsible for retrieving the contents from the database and returning them to GraphQL.

        :param self: Refers to the current instance of a class
        :param info: Pass along the context of the query
        :param content_id: Refers to the specific content object's id which needs to be returned
        :param last: Refers to the count of last records need to be returned
        :param offset: Refers to the count of how many records has already been returned
        :return: Last records starting from offset to last from the database
        """
        if not content:
            return Content.objects.all()\
                .order_by('-created_at')[offset:offset+last]
        return [Content.objects.get(id=content)]


class Mutation(graphene.ObjectType):
    create_content = CreateContent.Field()
    update_content = UpdateContent.Field()
    delete_content = DeleteContent.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)