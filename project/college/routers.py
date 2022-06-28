from rest_framework import routers, viewsets

from project.college.models import Lesson, Grade
from project.college.serializers import LessonSerializer, GradeSerializer


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer


college_api_router = routers.SimpleRouter()
college_api_router.register("lesson", LessonViewSet)
college_api_router.register("grade", GradeViewSet)
