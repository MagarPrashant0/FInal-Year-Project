from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from core.models import Student, Attendance

class Command(BaseCommand):
    help = 'Sends email to students absent for 3 consecutive days'

    def handle(self, *args, **options):
        today = timezone.now().date()
        # Define the last 3 days
        last_3_days = [today - timedelta(days=i) for i in range(1, 4)]

        students = Student.objects.all()

        for student in students:
            # Check if there is ANY attendance for this student in the last 3 days
            attendance_exists = Attendance.objects.filter(
                student=student,
                date__in=last_3_days
            ).exists()

            # If no record is found, they were absent for all 3 days
            if not attendance_exists:
                print(f"Sending email alert to: {student.name} ({student.email})")
                try:
                    send_mail(
                        'Absence Warning - Attendance System',
                        f'Dear {student.name},\n\nYou have been absent for the last 3 consecutive days. Please report to the administration.',
                        'alemagar523@gmail.com',
                        [student.email],
                        fail_silently=False,
                    )
                except Exception as e:
                    print(f"Error sending email to {student.name}: {e}")
