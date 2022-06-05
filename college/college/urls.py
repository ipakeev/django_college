from django.urls import path

from .views import (
    ChairListView,
    ChairDetailView,
    CourseListView,
    CourseDetailView,
    TimeTableView,
    LessonDetail,
)

app_name = "college"

urlpatterns = [
    path("chairs/", ChairListView.as_view(), name="chairs"),
    path("chairs/<int:pk>/", ChairDetailView.as_view(), name="chair_detail"),
    path("courses/", CourseListView.as_view(), name="courses"),
    path("courses/<int:pk>/", CourseDetailView.as_view(), name="course_detail"),
    path("courses/<int:pk>/timetable/", TimeTableView.as_view(), name="timetable"),
    path("lessons/<int:pk>/", LessonDetail.as_view(), name="lesson_detail"),
]
