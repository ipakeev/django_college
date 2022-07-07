import graphene

from project.college.gql.types import ChairType, CourseType
from project.college.models import Chair, Course


class CollegeQueries(graphene.ObjectType):
    chairs = graphene.List(ChairType)
    courses = graphene.List(CourseType)

    def resolve_chairs(self, info):
        return Chair.objects.all()

    def resolve_courses(self, info):
        return Course.objects.all()
