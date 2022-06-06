from django.urls import path

from .views import (
    ChairListView,
    ChairDetailView,
    CourseListView,
    CourseDetailView,
    TimeTableView,
    LessonDetailView,
    LessonCreateView,
    LessonUpdateView,
    LessonDeleteView,
)

app_name = "college"

urlpatterns = [
    path("courses/", CourseListView.as_view(), name="courses"),
    path("courses/<int:pk>/", CourseDetailView.as_view(), name="course_detail"),
    path("courses/<int:pk>/timetable/", TimeTableView.as_view(), name="timetable"),
    path("chairs/", ChairListView.as_view(), name="chairs"),
    path("chairs/<int:pk>/", ChairDetailView.as_view(), name="chair_detail"),
    path("chairs/<int:chair_pk>/lessons/<int:lesson_pk>/", LessonDetailView.as_view(), name="lesson_detail"),
    path("chairs/<int:chair_pk>/lessons/create/", LessonCreateView.as_view(), name="lesson_create"),
    path("chairs/<int:chair_pk>/lessons/<int:lesson_pk>/update/", LessonUpdateView.as_view(), name="lesson_update"),
    path("chairs/<int:chair_pk>/lessons/<int:lesson_pk>/delete/", LessonDeleteView.as_view(), name="lesson_delete"),
]
