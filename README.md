# Face Recognition Attendance System

A hybrid Desktop & Web application that uses Computer Vision to automate the attendance process.
Instead of manual roll calls, this system detects faces via a webcam, recognizes registered students using the LBPH Algorithm, and automatically syncs the attendance data to a Django + PostgreSQL backend server.

## Key Features

- Real-Time Face Recognition: Instantly identifies students via webcam.

#### Hybrid Architecture:

- Desktop App (Tkinter): For capturing images and marking attendance in the classroom.
- Web Dashboard (Django): For teachers/admins to manage students and view attendance reports.
- Database Integration: Uses PostgreSQL for secure and scalable data storage (replacing old CSV files).
- Multiple Attendance: Can detect and mark multiple students in a single session without duplication.
- Auto-Sync: New registrations and attendance logs are automatically sent from the Python app to the Server via API.

## Tech Stack

- Component Technology
- Frontend (Desktop) Python, Tkinter, Pillow
- Backend (Server) Django (Python Framework)
- Database PostgreSQL
- Computer Vision OpenCV (cv2)
- Algorithm LBPH (Local Binary Patterns Histograms)
- Communication REST API (requests module)

## Project Structure

- main.py: The Desktop Application (Camera & GUI).
- Backend_Server/: The Django Project folder containing the API and Admin Panel.
- TrainingImage/: Stores raw photos captured for training.
- TrainingImageLabel/: Stores the trained model (Trainner.yml).
- haarcascade_frontalface_default.xml: Pre-trained model required for face detection.

## Installation & Setup

#### Clone the Repository

      git clone https://github.com/MagarPrashant0/Final-Year-Project.git
      cd Final-Year-Project

#### Install Python Dependencies

You need libraries for both the Desktop App and the Django Server.
pip install opencv-contrib-python numpy pandas Pillow requests django psycopg2-binary

#### Setup the Database (PostgreSQL)

      Install PostgreSQL and create a database named attendance_db.
      Update Backend_Server/settings.py with your database password.

#### Run the Backend Server

      Open a terminal in the Backend_Server folder:
      python manage.py makemigrations
      python manage.py migrate
      python manage.py createsuperuser  # Create your Admin login
      python manage.py runserver
      Keep this terminal running.

#### Run the Desktop App

      Open a new terminal in the main folder:
      python main.py

## How to Use

#### Step 1: Register a New Student

      Enter ID and Name in the Tkinter App.
      Click "Take Images".
      The app captures 60-100 photos.
      It automatically sends the Student Details to the Django Database.
      Click "Save Profile".
      Enter the admin password to train the model.

#### Step 2: Mark Attendance

      Click "Take Attendance".
      The webcam opens. When a face is recognized:
      The Name is displayed on the screen.
      The status is updated from Absent to Present in the Database.
      Press 'q' or click the "X" to close.

#### Step 3: View Reports (Admin Panel)

      Open your browser and go to: http://127.0.0.1:8000/admin/
      Login with your superuser credentials.
      View the list of Students and daily Attendance logs.

#### Architecture Diagram

![Face recognization system architecture diagram ](image.png)

## How it Works (Logic Flow)

- Detection: OpenCV (Haar Cascade) finds a face in the video frame.
- Recognition: The LBPH algorithm compares the face against the trained Trainner.yml model.

## API Call:

- If a match is found, Python sends the Student ID to the Django Server via HTTP POST.
- Django updates the PostgreSQL database.
- Django responds with the Student Name, which is then shown on the camera screen.

## Important Notes

- LBPH Algorithm: We use cv2.face.LBPHFaceRecognizer because it is robust against lighting changes.
- PostgreSQL: Ensure the Postgres service is running before starting Django.
- Camera: If the camera doesn't open, ensure no other application (like Zoom) is using it.
