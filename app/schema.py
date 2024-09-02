import graphene
import user.schema
import user.schemas.current
import content.schema
import comment.schema
import feedback.schema


class Query(user.schema.Query,
            user.schemas.current.Query,
            content.schema.Query,
            comment.schema.Query,
            feedback.schema.Query,
            graphene.ObjectType):
    # Combine the queries from different apps
    pass


class Mutation(user.schemas.current.Mutation,
                content.schema.Mutation,
                comment.schema.Mutation,
                feedback.schema.Mutation,
                graphene.ObjectType):
    # Combine the mutations from different apps
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)