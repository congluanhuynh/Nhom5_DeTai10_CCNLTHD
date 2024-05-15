from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path
from . import dao

from .models import Major, Department, Thesis, Student, Score, User, Council, CouncilMembership, InterviewSchedule
from django.contrib.auth.models import Permission, ContentType, Group


class ThesisAppAdminSite(admin.AdminSite):
    site_header = 'Hệ thống quản lý khóa luận tốt nghiệp'

    def get_urls(self):
        return [
                   path('thesis-stats/', self.stats_view)
               ] + super().get_urls()

    def stats_view(self, request):
        return TemplateResponse(request, 'admin/stats_view.html', {
            'stats': dao.count_thesis_by_major()
        })


class ThesisStudentInlineAdmin(admin.TabularInline):
    model = Thesis.students.through


class ThesisInstructorInlineAdmin(admin.TabularInline):
    model = Thesis.users.through


class ThesisAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "major", "created_date"]
    list_filter = ["id", "major"]
    search_fields = ["name", "major__name"]
    inlines = [ThesisStudentInlineAdmin, ThesisInstructorInlineAdmin]


class StudentAdmin(admin.ModelAdmin):
    list_display = ["username", "first_name", "last_name", "major"]
    list_filter = ["username", "school_year", "major"]
    search_fields = ["username", "school_year", "major__name"]


class CouncilMembershipInlineAdmin(admin.StackedInline):
    model = CouncilMembership
    fk_name = 'council'


class CouncilAdmin(admin.ModelAdmin):
    inlines = [CouncilMembershipInlineAdmin]


class InterviewScheduleAdmin(admin.ModelAdmin):
    list_display = ["thesis", "time", "date", "location"]
    list_filter = ["thesis", "time", "date", "location"]


class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "username", "email" ]


class ScoreAdmin(admin.ModelAdmin):
    list_display = ["thesis", "user", "council", "score_value"]
    list_filter = ["thesis","council"]


# Register your models here.
admin_site = ThesisAppAdminSite(name= 'myadmin')
admin_site.register(Student, StudentAdmin)
admin_site.register(Major)
admin_site.register(Department)
admin_site.register(Council,CouncilAdmin)
admin_site.register(Thesis, ThesisAdmin)
admin_site.register(InterviewSchedule, InterviewScheduleAdmin)
admin_site.register(Score, ScoreAdmin)
admin_site.register(User, UserAdmin)
admin_site.register(Permission)
admin_site.register(Group)
admin_site.register(ContentType)
