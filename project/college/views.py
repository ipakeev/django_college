from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    View,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from project.application.permissions import ViewTimetablePermission, EditLessonsPermission
from .models import Chair, Course, TimeTable, Lesson


class ChairListView(ListView):
    model = Chair


class ChairDetailView(DetailView):
    model = Chair


class CourseListView(ListView):
    model = Course


class CourseDetailView(DetailView):
    model = Course


class TimeTableView(PermissionRequiredMixin, View):
    permission_required = ViewTimetablePermission.title

    def get(self, request, pk: int, *args, **kwargs):
        context = {
            "course": Course.objects.filter(pk=pk),
            "timetable": TimeTable.objects.filter(course_id=pk).select_related(
                "course", "lesson", "lesson__chair", "teacher", "auditorium"
            )
        }
        return render(request, "college/timetable.html", context=context)


class LessonCRUDMixin(PermissionRequiredMixin):
    kwargs: dict
    object: Lesson

    permission_required = EditLessonsPermission.title

    def get_object(self, queryset=None) -> Lesson:
        return Lesson.objects.filter(
            id=self.kwargs["lesson_pk"],
            chair_id=self.kwargs["chair_pk"],
        ).select_related("chair").first()

    def get_success_url(self):
        return reverse_lazy(
            "college:chair_detail",
            kwargs={"pk": self.object.chair.pk},
        )


class LessonDetailView(LessonCRUDMixin, DetailView):
    model = Lesson


class LessonCreateView(LessonCRUDMixin, CreateView):
    model = Lesson
    fields = ("theme", "homework")
    template_name_suffix = "_create_form"

    def form_valid(self, form):
        form.instance.chair_id = self.kwargs["chair_pk"]
        return super().form_valid(form)


class LessonUpdateView(LessonCRUDMixin, UpdateView):
    model = Lesson
    fields = ("theme", "homework")
    template_name_suffix = "_update_form"


class LessonDeleteView(LessonCRUDMixin, DeleteView):
    model = Lesson
    template_name_suffix = "_delete_form"
