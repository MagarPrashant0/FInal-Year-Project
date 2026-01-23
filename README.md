# Final Year Project

We have used the modules 
1.	**opencv-contrib-python (Used as cv2)** 
    This is the most important one. It handles the camera and face recognition.
    Just opencv-python does not support the cv2 face recognition. So, we must install the contrib version because our code uses cv2.face.LBPHFaceRecognizer, which is only included in the contrib package.
2.	**numpy (Used as np)**
    It handles math. Images are converted into number arrays so the computer can process them.
3.	**pandas (Used as pd)**
    It is used to read and manage the CSV files (where student details are stored) easily.
4.	**Pillow (Used as PIL)**
    It is used to open and convert images before passing them to the recognizer.
5. **Tkinter (GUI Interface)**
   This is used for the GUI interface which can make user easier to use. 


**Installed modules**
    Command for installation
    pip install opencv-contrib-python
    pip install numpy
    pip install pandas
    pip install Pillow 

**Use of Tkinter in our Project**
In our Attendance System, Tkinter acts as the "Front-End" (the face), while OpenCV acts as the "Back-End" (the brain).
Here are the specific Tkinter "Widgets" (tools) used in your code:
1. tk.Tk():
    This creates the Main Window (the container for everything).
    It controls the background color (#262523) and size (1280x720).
2. tk.Entry:
    These are the White Text Boxes where we type the Student ID and Name.
    The code reads what we typed using .get().
3. tk.Button:
    These are the buttons like "Take Images" or "Take Attendance".
    When we click them, they trigger a specific function (command) in our Python code.
4. tk.Label:
    These are the text headers like "Face Recognition Attendance System" or the clock.
    They display information that the user cannot change.
5. tk.messagebox:
    These are the Popup Windows.
    Example: When the camera fails or a password is saved, a small box pops up saying "Success" or "Error".
6. ttk.Treeview:
    This is the Table at the bottom of the screen.
    It displays the attendance list (ID, Name, Date, Time) in columns, looking like an Excel sheet.

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
# Important Notes
1. Lighting: Ensure good lighting when taking images and marking attendance for better accuracy.
2. Python Version: Recommended to use Python 3.10 or 3.11 for best compatibility with OpenCV. (Python 3.13 may have stability issues).
3. Camera: If the camera doesn't open, ensure no other app (like Zoom) is using it.






