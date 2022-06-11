from django.db.models import Prefetch
from django.views.generic import ListView, DetailView

from college.models import Course, Grade, TimeTable
from users.models import Teacher, Student


class TeacherListView(ListView):
    model = Teacher


class TeacherDetailView(DetailView):
    model = Teacher


class StudentListView(ListView):
    model = Student


class StudentDetailView(DetailView):
    model = Student

    def get_object(self, queryset=None) -> Student:
        return (
            Student.objects.filter(id=self.kwargs["pk"])
            .prefetch_related(
                Prefetch("courses", Course.objects.filter(students__id=self.kwargs["pk"])),
                Prefetch("grades", Grade.objects.filter(student_id=self.kwargs["pk"])),
                Prefetch("grades__timetable", TimeTable.objects.filter(course__students__id=self.kwargs["pk"])),
                Prefetch("grades__timetable__course", Course.objects.filter(students__id=self.kwargs["pk"])),
                "grades__timetable__lesson",
                "grades__timetable__lesson__chair",
            ).first()
        )
