GROUP_OAUTH2 = "OAuth2"
GROUP_TEACHER = "Teacher"
GROUP_STUDENT = "Student"


class BasePermissions:
    title: str
    description: str

    @classmethod
    @property
    def perm(cls) -> tuple[str, str]:
        return cls.title, cls.description


class EditLessonsPermission(BasePermissions):
    title = "edit_lessons"
    description = "Can create, edit, delete lessons."


class ViewStudentDetailsPermission(BasePermissions):
    title = "view_student_details"
    description = "Can view students' marks."


class ViewTimetablePermission(BasePermissions):
    title = "view_timetable"
    description = "Can read timetable."


class SendEmailPermission(BasePermissions):
    title = "send_email"
    description = "Can send email."


GROUPS_PERMISSIONS: dict[str, tuple[BasePermissions, ...]] = {
    GROUP_OAUTH2: (
        ViewTimetablePermission.title,
        SendEmailPermission.title,
    ),
    GROUP_TEACHER: (
        EditLessonsPermission.title,
        ViewStudentDetailsPermission.title,
        ViewTimetablePermission.title,
        SendEmailPermission.title,
    ),
    GROUP_STUDENT: (
        ViewStudentDetailsPermission.title,
        ViewTimetablePermission.title,
        SendEmailPermission.title,
    ),
}
