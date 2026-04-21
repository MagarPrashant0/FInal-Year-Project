from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
# Ensure the import is just 'core.models' to avoid the RuntimeWarning
from core.models import Student, Attendance

class Command(BaseCommand):
    help = 'Sends email to students who have zero "Present" records in the last 3 days'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("--- Starting Absence Check ---"))

        today = timezone.now().date()
        # Define the last 3 days (e.g., Yesterday, 2 days ago, 3 days ago)
        last_3_days = [today - timedelta(days=i) for i in range(1, 4)]

        self.stdout.write(f"Checking Attendance for dates: {last_3_days}")

        # Get all students from PostgreSQL
        students = Student.objects.all()
        self.stdout.write(f"Found {students.count()} students in database.")

        for student in students:
            # Check how many times this student was marked 'Present' in those 3 days
            present_count = Attendance.objects.filter(
                student=student,
                date__in=last_3_days,
                status='Present'
            ).count()

            # If they have 0 'Present' records, they are considered absent
            if present_count == 0:
                self.stdout.write(self.style.WARNING(f"Student {student.name} was NOT present in the last 3 days."))

                # Check if we have an email to send to
                if student.email:
                    self.stdout.write(f"Sending email to {student.email}...")
                    try:
                        send_mail(
                            subject='Absence Warning - Attendance Monitoring System',
                            message=(
                                f'Dear {student.name},\n\n'
                                f'Our records show you have not been present for the last 3 consecutive days.\n\n'
                                f'Please contact the administration office immediately.'
                            ),
                            from_email='alemagar523@gmail.com', # Must match EMAIL_HOST_USER in settings.py
                            recipient_list=[student.email],
                            fail_silently=False,
                        )
                        self.stdout.write(self.style.SUCCESS(f"Successfully sent email to {student.name}"))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Failed to send email to {student.name}: {e}"))
                else:
                    self.stdout.write(self.style.ERROR(f"Skipped {student.name}: No email address found in profile."))

            else:
                self.stdout.write(f"Student {student.name} was present {present_count} time(s). No action needed.")

        self.stdout.write(self.style.SUCCESS("--- Absence Check Completed ---"))
