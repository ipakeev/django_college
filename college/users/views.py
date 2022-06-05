from django.views.generic import ListView, DetailView

from users.models import Teacher, Student


class TeacherListView(ListView):
    model = Teacher


class TeacherDetailView(DetailView):
    model = Teacher


class StudentListView(ListView):
    model = Student


class StudentDetailView(DetailView):
    model = Student
