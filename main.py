############################################# IMPORTING ################################################
import requests
import json
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import cv2,os
import csv
import numpy as np
from PIL import Image, ImageTk, ImageEnhance
import pandas as pd
import datetime
import time
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # Ensure relative paths work by setting Current Working Directory (CWD) to the script's folder

############################################# FUNCTIONS ################################################
# Creates the directory for a given file path if it doesn't already exist
def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

# Updates the clock label with the current time every 200ms
def tick():
    time_string = time.strftime('%H:%M:%S')
    clock.config(text=time_string)
    clock.after(200, tick)

# Opens a popup window displaying contact information
def contact():
    mess._show(title='Contact us', message="Please contact us on : 'alemagar523@gmail.com' ")

# Verifies that the Haarcascade file exists in the current folder
def check_haarcascadefile():
    # Changed from hardcoded D:\ drive to relative path for portability
    path = "haarcascade_frontalface_default.xml"
    exists = os.path.isfile(path)
    if exists:
        pass
    else:
        mess._show(title='File Missing', message='The haarcascade file (haarcascade_frontalface_default.xml) is missing from the project folder!')
        window.destroy()
        return

def on_closing():
    if mess.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()
######################################### CLEAR FUNCTIONS ############################################

# Clears ID box
def clear():
    txt.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)

# Clears Name box
def clear2():
    txt2.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)

# Clears Email box (NEW)
def clear3():
    txt_email.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)

######################################### PASSWORD SYSTEM ############################################

def save_pass():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\\psd.txt", "r")
        key = tf.read()
    else:
        master.destroy()
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel\\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    op = (old.get())
    newp= (new.get())
    nnewp = (nnew.get())
    if (op == key):
        if(newp == nnewp):
            txf = open("TrainingImageLabel\\psd.txt", "w")
            txf.write(newp)
        else:
            mess._show(title='Error', message='Confirm new password again!!!')
            return
    else:
        mess._show(title='Wrong Password', message='Please enter correct old password.')
        return
    mess._show(title='Password Changed', message='Password changed successfully!!')
    master.destroy()

def change_pass():
    global master
    master = tk.Tk()
    master.geometry("400x160")
    master.resizable(False,False)
    master.title("Change Password")
    master.configure(background="white")

    lbl4 = tk.Label(master,text='    Enter Old Password',bg='white',font=('times', 12, ' bold '))
    lbl4.place(x=10,y=10)
    global old
    old=tk.Entry(master,width=25 ,fg="black",relief='solid',font=('times', 12, ' bold '),show='*')
    old.place(x=180,y=10)

    lbl5 = tk.Label(master, text='   Enter New Password', bg='white', font=('times', 12, ' bold '))
    lbl5.place(x=10, y=45)
    global new
    new = tk.Entry(master, width=25, fg="black",relief='solid', font=('times', 12, ' bold '),show='*')
    new.place(x=180, y=45)

    lbl6 = tk.Label(master, text='Confirm New Password', bg='white', font=('times', 12, ' bold '))
    lbl6.place(x=10, y=80)
    global nnew
    nnew = tk.Entry(master, width=25, fg="black", relief='solid',font=('times', 12, ' bold '),show='*')
    nnew.place(x=180, y=80)

    cancel=tk.Button(master,text="Cancel", command=master.destroy ,fg="black"  ,bg="red" ,height=1,width=25 , activebackground = "white" ,font=('times', 10, ' bold '))
    cancel.place(x=200, y=120)
    save1 = tk.Button(master, text="Save", command=save_pass, fg="black", bg="#3ece48", height = 1,width=25, activebackground="white", font=('times', 10, ' bold '))
    save1.place(x=10, y=120)
    master.mainloop()

# Function for "Save Profile" button
def psw():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\\psd.txt")

    # 1. Get the key or create a new one if it's the first time
    if exists1:
        with open("TrainingImageLabel\\psd.txt", "r") as tf:
            key = tf.read()
    else:
        new_pas = tsd.askstring('Password Not Found', 'Please enter a new admin password', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
            return
        else:
            with open("TrainingImageLabel\\psd.txt", "w") as tf:
                tf.write(new_pas)
            mess._show(title='Password Registered', message='New password registered successfully!!')
            return

    # 2. Ask for password before Training
    password = tsd.askstring('Password Required', 'Enter Admin Password', show='*')
    if (password == key):
        TrainImages()  # Start the training process
    elif (password == None):
        pass
    else:
        mess._show(title='Wrong Password', message='You have entered wrong password')


# Function for "Take Images" button
def psw_take():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\\psd.txt")

    # 1. Get the key or create a new one if it's the first time
    if exists1:
        with open("TrainingImageLabel\\psd.txt", "r") as tf:
            key = tf.read()
    else:
        new_pas = tsd.askstring('Password Not Found', 'Please enter a new admin password', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
            return
        else:
            with open("TrainingImageLabel\\psd.txt", "w") as tf:
                tf.write(new_pas)
            mess._show(title='Password Registered', message='New password registered successfully!!')
            return

    # 2. Ask for password before Camera opens
    password = tsd.askstring('Password Required', 'Enter Password to Register Student', show='*')
    if (password == key):
        TakeImages()  # Start the image capture process
    elif (password == None):
        pass
    else:
        mess._show(title='Wrong Password', message='You have entered wrong password')

def update_registration_count():
    global message
    try:
        # Request the latest count from your Django PostgreSQL database
        response = requests.get("http://127.0.0.1:8000/api/get_student_count/")
        if response.status_code == 200:
            count = response.json().get('count', 0)
            message.configure(text='Total Registrations till now : ' + str(count))
        else:
            message.configure(text='Total Registrations till now : Error')
    except Exception as e:
        # If the server is offline, fallback to the local CSV count
        print(f"Server Offline: {e}")
        res = 0
        if os.path.isfile("StudentDetails\\StudentDetails.csv"):
            with open("StudentDetails\\StudentDetails.csv", 'r') as f:
                res = sum(1 for row in csv.reader(f))
            res = (res // 2) - 1
        message.configure(text='Total Registrations till now : ' + str(max(0, res)))

#######################################################################################
# Captures 100 face samples via webcam, saves them to the training folder, and updates the student database (CSV)
def TakeImages():
    check_haarcascadefile()

    # 1. Get Data from the GUI Entry boxes
    Id = txt.get()
    name = txt2.get()
    email = txt_email.get() # The new email field

    # 2. Basic Validation
    if not Id or not name or not email:
        mess._show(title='Missing Data', message='Please enter ID, Name, and Email!')
        return

    # Check if name is valid (alphabetical)
    if (name.replace(' ', '').isalpha()):
        assure_path_exists("TrainingImage/")
        assure_path_exists("StudentDetails/")

        # 3. Setup Camera
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0

        # Calculate a local serial number for the filename
        serial = 0
        exists = os.path.isfile("StudentDetails\\StudentDetails.csv")
        if exists:
            with open("StudentDetails\\StudentDetails.csv", 'r') as f:
                serial = sum(1 for line in f) // 2
        else:
            serial = 1

        # 4. Capture 100 Face Samples
        while True:
            ret, img = cam.read()
            if not ret: break
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                sampleNum += 1
                # Save the captured image in the TrainingImage folder
                cv2.imwrite(f"TrainingImage\\{name}.{serial}.{Id}.{sampleNum}.jpg", gray[y:y + h, x:x + w])
                cv2.imshow('Taking Images', img)

            if cv2.waitKey(100) & 0xFF == ord('q') or sampleNum > 100:
                break

        cam.release()
        cv2.destroyAllWindows()

        # 5. SYNC WITH DJANGO BACKEND
        try:
            API_URL = "http://127.0.0.1:8000/api/add_student/"
            payload = {
                'student_id': Id,
                'name': name,
                'email': email
            }
            # Send the data to PostgreSQL via Django
            response = requests.post(API_URL, json=payload)

            if response.status_code == 200:
                print(f"Student {name} successfully synced to Database.")
            else:
                print("Failed to sync with server.")
        except Exception as e:
            print(f"Server Connection Error: {e}")

        # 6. SAVE LOCALLY TO CSV (Fallback/Backup)
        row = [serial, '', Id, '', name]
        with open('StudentDetails\\StudentDetails.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)

        # 7. UPDATE THE UI COUNTER
        # This calls the function we wrote above to refresh the "Total Registrations" label
        update_registration_count()

        message1.configure(text=f"Images Saved for ID: {Id}")

    else:
        mess._show(title='Invalid Name', message='Please enter a valid alphabetical name.')

########################################################################################
# Reads all training images, trains the LBPH algorithm, and saves the model as 'Trainner.yml'
def TrainImages():
    check_haarcascadefile()
    assure_path_exists("TrainingImageLabel/")
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    path = "TrainingImage"
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces, Ids = [], []

    for imagePath in imagePaths:
        pilImage = Image.open(imagePath).convert('L')
        imageNp = np.array(pilImage, 'uint8')
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        faces.append(imageNp)
        Ids.append(ID)

    if not faces:
        mess._show(title='No Data', message='Register someone first!')
        return

    recognizer.train(faces, np.array(Ids))
    recognizer.save("TrainingImageLabel/Trainner.yml")
    message1.configure(text="Profile Saved Successfully")
############################################################################################3

def getImagesAndLabels(path):
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empth face list
    faces = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids

###########################################################################################
# Runs the webcam to recognize faces, matches them to the database, and saves the attendance record to a daily CSV file
def TrackImages():
    # 1. Clear the table on the left before starting
    check_haarcascadefile()
    for k in tv.get_children():
        tv.delete(k)

    # 2. Tell Django to start a new session (Mark everyone absent for today)
    try:
        requests.get("http://127.0.0.1:8000/api/start_session/")
        print("Session Started: All students marked absent initially.")
    except:
        print("Backend Server is offline. Attendance will not be saved to Database.")

    # 3. Load the Face Recognizer
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    if os.path.isfile("TrainingImageLabel\\Trainner.yml"):
        recognizer.read("TrainingImageLabel\\Trainner.yml")
    else:
        mess._show(title='Data Missing', message='Please click "Save Profile" to train the system first!')
        return

    # 4. Initialize Camera and Font
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX

    # These lists keep track of who we already recognized in THIS session
    marked_ids = []
    id_to_name = {}

    while True:
        ret, im = cam.read()
        if not ret: break

        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)

        for (x, y, w, h) in faces:
            # Draw the box around the face
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)

            # Predict the ID
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])

            # Check if the match is good (Confidence < 85 is usually a good match)
            if conf < 85:
                detected_id = str(serial)

                # --- STEP A: If it's a NEW recognition, sync with Django ---
                if detected_id not in marked_ids:
                    try:
                        API_URL = "http://127.0.0.1:8000/api/mark_attendance/"
                        response = requests.post(API_URL, json={'student_id': detected_id})

                        if response.status_code == 200:
                            data = response.json()
                            actual_name = data.get('name', 'Unknown')

                            # Save name in memory so we can show it on the screen
                            id_to_name[detected_id] = actual_name

                            # Add to the UI Table on the left
                            ts = time.time()
                            timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                            tv.insert('', 0, text=detected_id, values=(actual_name, "Today", timeStamp))

                            # Add to marked list so we don't spam the server
                            marked_ids.append(detected_id)
                    except Exception as e:
                        print(f"Error syncing attendance for ID {detected_id}: {e}")
                        id_to_name[detected_id] = f"ID: {detected_id}"

                # --- STEP B: Show the Name on the Video Feed ---
                # Get the name from our dictionary (memory)
                display_name = id_to_name.get(detected_id, "Processing...")
                cv2.putText(im, display_name, (x, y + h + 30), font, 1, (255, 255, 255), 2)

            else:
                # If confidence is bad, show "Unknown" in Red
                cv2.putText(im, "Unknown", (x, y + h + 30), font, 1, (0, 0, 255), 2)

        # Show the camera window
        cv2.imshow('Attendance System - Press Q to Quit', im)

        # Break loop if 'q' is pressed
        if cv2.waitKey(1) == ord('q'):
            break

    # 5. Cleanup
    cam.release()
    cv2.destroyAllWindows()

    # 6. TRIGGER THE AUTOMATED EMAIL CHECK
    # This calls the Django script to check for 3-day absences
    print("Camera closed. Checking for 3-day absences and sending emails...")
    try:
        email_res = requests.get("http://127.0.0.1:8000/api/run_email_check/")
        if email_res.status_code == 200:
            print("Server Response:", email_res.json().get('message'))
        else:
            print("Server encountered an error while processing emails.")
    except:
        print("Backend server unreachable for email processing.")

######################################## USED STUFFS ############################################
# Initialize global variables and setup date formatting (Number to Month Name)
global key
key = ''

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day,month,year=date.split("-")

mont={'01':'January',
      '02':'February',
      '03':'March',
      '04':'April',
      '05':'May',
      '06':'June',
      '07':'July',
      '08':'August',
      '09':'September',
      '10':'October',
      '11':'November',
      '12':'December'
      }

######################################## GUI FRONT-END ###########################################
# Sets up the main GUI window, defines layout frames (Left/Right), input fields, and calculates total registered users on startup
window = tk.Tk()
window.geometry("1280x720")
window.resizable(False, False)
window.title("Attendance Management System Pro")

# --- MODERN COLOR PALETTE ---
BG_MAIN = "#0b0d17"         # Deep Midnight
BG_CARD = "#161b22"         # Slate Card Color (GitHub Dark style)
ACCENT_BLUE = "#3498db"     # Professional Blue
ACCENT_GREEN = "#2ecc71"    # Professional Green
ACCENT_RED = "#e74c3c"      # Professional Red
TEXT_LIGHT = "#e6edf3"      # Off-white text
# --- 1. MAIN BACKGROUND IMAGE ---
try:
    # Load background, darken it by 60% for better contrast, and resize
    raw_bg = Image.open("background.jpg")
    enhancer = ImageEnhance.Brightness(raw_bg)
    darkened_bg = enhancer.enhance(0.4)
    resized_bg = darkened_bg.resize((1280, 720), Image.LANCZOS)
    bg_img = ImageTk.PhotoImage(resized_bg)

    bg_label = tk.Label(window, image=bg_img)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
except:
    window.configure(background=BG_MAIN)

# --- 2. HEADER BAR (Title, Date, and Orange Clock) ---
header = tk.Frame(window, bg="#000000", height=80)
header.pack(side="top", fill="x")

# Main Title
tk.Label(header, text="FACIAL RECOGNITION SYSTEM",
         fg=ACCENT_BLUE, bg="#000000", font=("Helvetica", 26, "bold")).place(x=30, y=15)

# Date and Clock (Top Right)
date_label = tk.Label(header, text="", fg="#aaaaaa", bg="#000000", font=("Helvetica", 12, "bold"))
date_label.place(x=1080, y=15)

clock = tk.Label(header, text="", fg="orange", bg="#000000", font=("Helvetica", 22, "bold"))
clock.place(x=1080, y=35)

# --- 3. LEFT CARD (Live Attendance Log) ---
frame1 = tk.Frame(window, bg=BG_CARD, highlightbackground=ACCENT_BLUE, highlightthickness=1)
frame1.place(x=30, y=110, width=580, height=580)

# CCTV Icon
try:
    img_a = Image.open("icon_attendance.png").resize((80, 80), Image.LANCZOS)
    render_a = ImageTk.PhotoImage(img_a)
    lbl_icon1 = tk.Label(frame1, image=render_a, bg=BG_CARD)
    lbl_icon1.image = render_a # Reference to prevent garbage collection
    lbl_icon1.pack(pady=(15, 0))
except: pass

tk.Label(frame1, text="LIVE MONITORING", fg=ACCENT_BLUE, bg=BG_CARD, font=("Helvetica", 14, "bold")).pack(pady=5)

# Camera Button
trackImg = tk.Button(frame1, text="START CAMERA", command=TrackImages,
                     fg="white", bg=ACCENT_BLUE, width=25, font=("Helvetica", 13, "bold"),
                     activebackground="#2980b9", bd=0, cursor="hand2")
trackImg.pack(pady=10)

# Styled Treeview (Table)
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background=BG_CARD, foreground=TEXT_LIGHT, fieldbackground=BG_CARD, rowheight=35, borderwidth=0)
style.configure("Treeview.Heading", background="#21262d", foreground=ACCENT_BLUE, font=("Helvetica", 11, "bold"), borderwidth=1)
style.map("Treeview", background=[('selected', "#238636")])

tv = ttk.Treeview(frame1, height=10, columns=('name', 'date', 'time'))
tv.column('#0', width=60); tv.column('name', width=130); tv.column('date', width=110); tv.column('time', width=110)
tv.heading('#0', text='ID'); tv.heading('name', text='NAME'); tv.heading('date', text='DATE'); tv.heading('time', text='TIME')
tv.place(x=30, y=210, width=520, height=300)

# Exit Button
quitWindow = tk.Button(frame1, text="EXIT SYSTEM", command=on_closing,
                       fg="#8b949e", bg="#21262d", width=25, font=("Helvetica", 11, "bold"), bd=0, cursor="hand2")
quitWindow.place(x=160, y=530)

# --- 4. RIGHT CARD (Student Registration) ---
frame2 = tk.Frame(window, bg=BG_CARD, highlightbackground=ACCENT_GREEN, highlightthickness=1)
frame2.place(x=660, y=110, width=580, height=580)

# Face Recognition Icon
try:
    img_r = Image.open("icon_registration.png").resize((80, 80), Image.LANCZOS)
    render_r = ImageTk.PhotoImage(img_r)
    lbl_icon2 = tk.Label(frame2, image=render_r, bg=BG_CARD)
    lbl_icon2.image = render_r
    lbl_icon2.pack(pady=(15, 0))
except: pass

tk.Label(frame2, text="USER ENROLLMENT", fg=ACCENT_GREEN, bg=BG_CARD, font=("Helvetica", 14, "bold")).pack(pady=5)

# Helper function for Input Fields
def create_entry_group(parent, label_text, y_pos):
    tk.Label(parent, text=label_text, fg="#8b949e", bg=BG_CARD, font=("Helvetica", 10, "bold")).place(x=60, y=y_pos)
    ent = tk.Entry(parent, font=("Helvetica", 13), bg="#0d1117", fg=TEXT_LIGHT, bd=0, insertbackground="white")
    ent.place(x=60, y=y_pos+22, width=380, height=32)
    # Modern underline
    tk.Frame(parent, bg="#30363d", height=2).place(x=60, y=y_pos+54, width=380)
    return ent

txt = create_entry_group(frame2, "STUDENT ID", 150)
txt2 = create_entry_group(frame2, "FULL NAME", 215)
txt_email = create_entry_group(frame2, "EMAIL ADDRESS", 280)

# Clear Buttons
tk.Button(frame2, text="Clear", command=clear, fg=ACCENT_BLUE, bg=BG_CARD, bd=0, font=("Helvetica", 9, "bold")).place(x=450, y=172)
tk.Button(frame2, text="Clear", command=clear2, fg=ACCENT_BLUE, bg=BG_CARD, bd=0, font=("Helvetica", 9, "bold")).place(x=450, y=237)
tk.Button(frame2, text="Clear", command=clear3, fg=ACCENT_BLUE, bg=BG_CARD, bd=0, font=("Helvetica", 9, "bold")).place(x=450, y=302)

# Action Buttons
takeImg = tk.Button(frame2, text="CAPTURE FACE", command=psw_take,
                    fg="white", bg="#238636", width=34, font=("Helvetica", 13, "bold"), bd=0, cursor="hand2")
takeImg.place(x=60, y=370)

trainImg = tk.Button(frame2, text="SAVE PROFILE", command=psw,
                     fg="white", bg="#1f6feb", width=34, font=("Helvetica", 13, "bold"), bd=0, cursor="hand2")
trainImg.place(x=60, y=430)

# Registration Counter Label
message = tk.Label(frame2, text="Total Registrations: 0", bg=BG_CARD, fg="#8b949e", font=("Helvetica", 11, "italic"))
message.place(x=200, y=510)

# --- 5. INITIALIZE GUI LOGIC ---
window.protocol("WM_DELETE_WINDOW", on_closing)
tick()                        # Start live clock
update_registration_count()    # Fetch count from Django
window.mainloop()

##################### MENUBAR #################################

menubar = tk.Menu(window,relief='ridge')
filemenu = tk.Menu(menubar,tearoff=0)
filemenu.add_command(label='Change Password', command = change_pass)
filemenu.add_command(label='Contact Us', command = contact)
filemenu.add_command(label='Exit',command = window.destroy)
menubar.add_cascade(label='Help',font=('times', 29, ' bold '),menu=filemenu)

################## TREEVIEW ATTENDANCE TABLE ####################

tv= ttk.Treeview(frame1,height =13,columns = ('name','date','time'))
tv.column('#0',width=82)
tv.column('name',width=130)
tv.column('date',width=133)
tv.column('time',width=133)
tv.grid(row=2,column=0,padx=(0,0),pady=(150,0),columnspan=4)
tv.heading('#0',text ='ID')
tv.heading('name',text ='NAME')
tv.heading('date',text ='DATE')
tv.heading('time',text ='TIME')

###################### SCROLLBAR ################################

scroll=ttk.Scrollbar(frame1,orient='vertical',command=tv.yview)
scroll.grid(row=2,column=4,padx=(0,100),pady=(150,0),sticky='ns')
tv.configure(yscrollcommand=scroll.set)

################################################################### BUTTON ###################################################
# --- CLEAR BUTTONS ---
# Clear ID
clearButton = tk.Button(frame2, text="Clear", command=clear, fg="black", bg="#ea2a2a", width=11, activebackground="white", font=('times', 11, ' bold '))
clearButton.place(x=335, y=73)

# Clear Name
clearButton2 = tk.Button(frame2, text="Clear", command=clear2, fg="black", bg="#ea2a2a", width=11, activebackground="white", font=('times', 11, ' bold '))
clearButton2.place(x=335, y=148)

# Clear Email
clearButton3 = tk.Button(frame2, text="Clear", command=clear3, fg="black", bg="#ea2a2a", width=11, activebackground="white", font=('times', 11, ' bold '))
clearButton3.place(x=335, y=223)

# --- ACTION BUTTONS (Right Frame) ---
# This button now requires a password via 'psw_take'
takeImg = tk.Button(frame2, text="Take Images", command=psw_take, fg="white", bg="blue", width=34, height=1, activebackground="white", font=('times', 15, ' bold '))
takeImg.place(x=30, y=325)

# This button requires a password via 'psw'
trainImg = tk.Button(frame2, text="Save Profile", command=psw, fg="white", bg="blue", width=34, height=1, activebackground="white", font=('times', 15, ' bold '))
trainImg.place(x=30, y=395)

# --- ATTENDANCE & SYSTEM BUTTONS (Left Frame) ---
trackImg = tk.Button(frame1, text="Take Attendance", command=TrackImages, fg="black", bg="yellow", width=35, height=1, activebackground="white", font=('times', 15, ' bold '))
trackImg.place(x=30, y=50)

# This button now calls 'on_closing' for a safe exit
quitWindow = tk.Button(frame1, text="Quit", command=on_closing, fg="black", bg="red", width=35, height=1, activebackground="white", font=('times', 15, ' bold '))
quitWindow.place(x=30, y=450)

##################### END ######################################

window.configure(menu=menubar)

update_registration_count()
window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()

####################################################################################################
