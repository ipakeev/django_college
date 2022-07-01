from django.urls import path

from .views import (
    AccountView,
    ContactsView,
    LoginView,
    LoginJWTView,
    LogoutView,
    TeacherListView,
    TeacherDetailView,
    StudentListView,
    StudentDetailView,
)

app_name = "users"

urlpatterns = [
    path("teachers/", TeacherListView.as_view(), name="teachers"),
    path("teachers/<int:pk>/", TeacherDetailView.as_view(), name="teacher_detail"),
    path("students/", StudentListView.as_view(), name="students"),
    path("students/<int:pk>/", StudentDetailView.as_view(), name="student_detail"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("login_jwt/", LoginJWTView.as_view(), name="login_jwt"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("account/", AccountView.as_view(), name="account"),
]
