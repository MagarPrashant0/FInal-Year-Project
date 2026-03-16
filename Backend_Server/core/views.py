from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Student, Attendance
import json
from datetime import date
from django.utils import timezone
from django.core.management import call_command

@csrf_exempt
def add_student_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        student_id = data.get('student_id')
        name = data.get('name')

        obj, created = Student.objects.get_or_create(student_id=student_id, defaults={'name': name})
        if not created:
            obj.name = name
            obj.save()
        return JsonResponse({'status': 'success'})

@csrf_exempt
def start_session_api(request):
    students = Student.objects.all()
    today = date.today()
    count = 0
    for s in students:
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
            student_id = str(data.get('student_id'))
            student = Student.objects.get(student_id=student_id)
            today = date.today()
            attendance_record = Attendance.objects.filter(student=student, date=today).first()

            if attendance_record:
                attendance_record.status = 'Present'
                attendance_record.time = timezone.now()
                attendance_record.save()
                msg = "Updated Absent to Present"
            else:
                Attendance.objects.create(student=student, status='Present')
                msg = "Created new Present record"

            return JsonResponse({'status': 'success', 'name': student.name, 'message': msg})
        except Student.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': f'Student ID {student_id} not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

@csrf_exempt
def trigger_absence_check(request):
    try:
        call_command('check_absent')
        return JsonResponse({'status': 'success', 'message': 'Email check completed.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
