from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Student, Attendance
import json
from datetime import date
from django.utils import timezone

@csrf_exempt
def add_student_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        student_id = data.get('student_id')
        name = data.get('name')

        # This line saves it to PostgreSQL
        obj, created = Student.objects.get_or_create(student_id=student_id, defaults={'name': name})

        if not created:
            obj.name = name # Update name if ID exists
            obj.save()

        return JsonResponse({'status': 'success'})

# --- NEW FUNCTION: MARK EVERYONE ABSENT FIRST ---
@csrf_exempt
def start_session_api(request):
    # This runs when you open the camera.
    # It checks every student. If they don't have a record for today, mark them ABSENT.
    students = Student.objects.all()
    today = date.today()

    count = 0
    for s in students:
        # get_or_create checks if a record exists.
        # If NO record exists, it creates one with status='Absent'
        obj, created = Attendance.objects.get_or_create(
            student=s,
            date=today,
            defaults={'status': 'Absent', 'time': timezone.now()}
        )
        if created:
            count += 1

    return JsonResponse({'status': 'success', 'message': f'{count} students marked Absent initially.'})

@csrf_exempt
def mark_attendance_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            student_id = str(data.get('student_id')) # Convert to string to be safe

            # 1. Find the Student
            student = Student.objects.get(student_id=student_id)
            today = date.today()

            # 2. Find the existing 'Absent' record for today
            # We use .filter().first() to avoid crashing if it doesn't exist
            attendance_record = Attendance.objects.filter(student=student, date=today).first()

            if attendance_record:
                # UPDATE EXISTING RECORD
                attendance_record.status = 'Present'
                attendance_record.time = timezone.now()
                attendance_record.save()
                msg = "Updated Absent to Present"
            else:
                # CREATE NEW RECORD (If start_session wasn't run)
                Attendance.objects.create(
                    student=student,
                    status='Present'
                )
                msg = "Created new Present record"

            return JsonResponse({'status': 'success', 'name': student.name, 'message': msg})

        except Student.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': f'Student ID {student_id} not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
