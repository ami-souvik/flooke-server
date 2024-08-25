import graphene
import content.schema


class Query(content.schema.Query, graphene.ObjectType):
    # Combine the queries from different apps
    pass


class Mutation(content.schema.Mutation, graphene.ObjectType):
    # Combine the mutations from different apps
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)