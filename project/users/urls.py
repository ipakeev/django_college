from django.urls import path

from .views import TeacherListView, TeacherDetailView, StudentListView, StudentDetailView, Contacts

app_name = "users"

urlpatterns = [
    path("teachers/", TeacherListView.as_view(), name="teachers"),
    path("teachers/<int:pk>/", TeacherDetailView.as_view(), name="teacher_detail"),
    path("students/", StudentListView.as_view(), name="students"),
    path("students/<int:pk>/", StudentDetailView.as_view(), name="student_detail"),
    path("contacts/", Contacts.as_view(), name="contacts"),
]
