from django.contrib import admin
from .models import Student, Attendance

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'time', 'status')
    list_filter = ('date', 'student')

admin.site.register(Student)
admin.site.register(Attendance, AttendanceAdmin)
