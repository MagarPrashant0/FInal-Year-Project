from django.contrib import admin
from .models import Student, Attendance
class StudentAdmin(admin.ModelAdmin):
    # Columns to show in the list
    list_display = ('student_id', 'name', 'email')

    search_fields = ('name', 'student_id')

    # Order them by ID
    ordering = ('student_id',)

class AttendanceAdmin(admin.ModelAdmin):

    list_display = ('get_student_name', 'get_student_id', 'date', 'time', 'status')

    list_filter = ('date', 'status')

    search_fields = ('student__name', 'student__student_id')

    def get_student_name(self, obj):
        return obj.student.name
    get_student_name.short_description = 'Student Name'

    def get_student_id(self, obj):
        return obj.student.student_id
    get_student_id.short_description = 'ID'

admin.site.register(Student, StudentAdmin)
admin.site.register(Attendance, AttendanceAdmin)
