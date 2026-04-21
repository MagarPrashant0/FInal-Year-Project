from django.db import models

class Student(models.Model):
    # ... your existing fields ...python manage.py makemigrations
    last_email_sent = models.DateField(null=True, blank=True)

class Student(models.Model):
    student_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, null=True, blank=True)

    # --- ADD THIS LINE ---
    last_email_sent = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.student_id} - {self.name}"
class Attendance(models.Model):
    # Use 'core.Student' instead of just 'Student'
    student = models.ForeignKey('core.Student', on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Present')
    def __str__(self):
        return f"{self.student.name} - {self.date}"

