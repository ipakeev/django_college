from django.shortcuts import render, get_object_or_404
from django.views.generic import View, ListView, DetailView

from .models import Chair, Course, TimeTable, Lesson


class ChairListView(ListView):
    model = Chair


class ChairDetailView(DetailView):
    model = Chair


class CourseListView(ListView):
    model = Course


class CourseDetailView(DetailView):
    model = Course


class TimeTableView(View):

    def get(self, request, pk: int, *args, **kwargs):
        context = {
            "course": get_object_or_404(Course, pk=pk),
            "timetable": TimeTable.objects.filter(course_id=pk).all(),
        }
        return render(request, "college/timetable.html", context=context)


class LessonDetail(DetailView):
    model = Lesson
