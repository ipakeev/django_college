import graphene

from project.college.gql.queries import CollegeQueries


class Query(CollegeQueries, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
