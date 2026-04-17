# Face Recognition Attendance System

A desktop application that uses Computer Vision to automate the attendance process. Instead of manual roll calls, this system detects faces via a webcam, recognizes registered students, and marks their attendance in an Excel-compatible (CSV) file.

## Features

    GUI Interface: Easy-to-use interface built with Tkinter.
    Data Collection: Automated capturing of face images for new registrations.
    Model Training: Uses the LBPH (Local Binary Patterns Histograms) algorithm to train the model.
    Real-Time Recognition: Detects and identifies faces instantly via webcam.
    Auto-Logging: Saves attendance details (ID, Name, Date, Time) automatically into a CSV file.

## Tech Stack

    Language: Python
    Interface: Tkinter
    Computer Vision: OpenCV (cv2)
    Data Handling: Pandas, Numpy, CSV
    Image Processing: Pillow (PIL)

## Project Structure

    When you run the project, it automatically creates these necessary folders:
    TrainingImage/: Stores the raw photos taken for training.
    TrainingImageLabel/: Stores the trained model (Trainner.yml) and password file.
    StudentDetails/: Contains the list of registered students.
    Attendance/: Contains the daily attendance logs.

## Installation & Setup

Clone the Repository (or download the files).

### Install Required Libraries:

Open your terminal/command prompt and run:

### code

pip install opencv-contrib-python numpy pandas Pillow
(Note: You must use opencv-contrib-python to access the Face Recognizer).

### Haar Cascade File:

    Ensure the file haarcascade_frontalface_default.xml is present in the main project folder. This file is required to detect faces.

## How to Use

Run the Application:

### code

python main.py

### Register a New Student:

    Enter ID and Name in the text boxes.
    Click "Take Images". The webcam will open and take samples of your face.
    Click "Save Profile". You will be asked for a password (to prevent unauthorized training). This processes the images and trains the model.

### Mark Attendance:

    Click "Take Attendance".
    The webcam will open. If your face is recognized, your name will appear on the screen.
    The attendance is automatically saved to the Attendance/ folder.
    Press q or click the "STOP" button (if enabled) to close the camera.

## How it Works

1. Face Detection: The system uses Haarcascade to find a face in the frame (converting it to grayscale).
2. Feature Extraction: It crops the face and saves it.
3. Training: The LBPH algorithm analyzes the saved photos and creates a mathematical model (Trainner.yml).
4. Recognition: When taking attendance, the live video is compared against the Trainner.yml model to find a match.
