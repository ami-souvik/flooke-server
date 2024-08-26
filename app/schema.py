import graphene
import basic_auth.schema
import content.schema
import comment.schema


class Query(basic_auth.schema.Query,
            content.schema.Query,
            comment.schema.Query,
            graphene.ObjectType):
    # Combine the queries from different apps
    pass


class Mutation(content.schema.Mutation,
                comment.schema.Mutation,
                graphene.ObjectType):
    # Combine the mutations from different apps
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)