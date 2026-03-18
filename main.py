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
from PIL import Image
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

def psw():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\\psd.txt", "r")
        key = tf.read()
    else:
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel\\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    password = tsd.askstring('Password', 'Enter Password', show='*')
    if (password == key):
        TrainImages()
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
    check_haarcascadefile()
    for k in tv.get_children(): tv.delete(k)

    # Start Session API
    try: requests.get("http://127.0.0.1:8000/api/start_session/")
    except: print("Server offline")

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    if not os.path.isfile("TrainingImageLabel/Trainner.yml"):
        mess._show(title='Missing Data', message='Please Train Profile first!')
        return

    recognizer.read("TrainingImageLabel/Trainner.yml")
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    marked_ids = []

    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if conf < 85:
                detected_id = str(serial)
                if detected_id not in marked_ids:
                    try:
                        res = requests.post("http://127.0.0.1:8000/api/mark_attendance/", json={'student_id': detected_id})
                        if res.status_code == 200:
                            data = res.json()
                            actual_name = data['name']
                            tv.insert('', 0, text=detected_id, values=(actual_name, "Today", time.strftime('%H:%M:%S')))
                            marked_ids.append(detected_id)
                            cv2.putText(im, actual_name, (x, y + h), font, 1, (255, 255, 255), 2)
                    except: pass
            else:
                cv2.putText(im, "Unknown", (x, y + h), font, 1, (255, 255, 255), 2)

        cv2.imshow('Attendance System', im)
        if cv2.waitKey(1) == ord('q'): break

    cam.release()
    cv2.destroyAllWindows()

    # --- EMAIL AUTOMATION TRIGGER ---
    print("Triggering Absence Check...")
    try:
        requests.get("http://127.0.0.1:8000/api/run_email_check/")
        print("Emails Processed.")
    except:
        print("Could not reach email server.")

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
window.title("Attendance System")
window.configure(background='#262523')

# Frames
frame1 = tk.Frame(window, bg="#00aeff")
frame1.place(relx=0.11, rely=0.17, relwidth=0.39, relheight=0.80)

frame2 = tk.Frame(window, bg="#00aeff")
frame2.place(relx=0.51, rely=0.17, relwidth=0.38, relheight=0.80)

# Labels
tk.Label(window, text="Face Recognition Based Attendance System", fg="white", bg="#262523", font=('times', 29, ' bold ')).place(x=10, y=10)
tk.Label(frame1, text="--- For Already Registered ---", fg="black", bg="#3ece48", font=('times', 17, ' bold ')).place(x=100, y=0)
tk.Label(frame2, text="--- For New Registrations ---", fg="black", bg="#3ece48", font=('times', 17, ' bold ')).place(x=100, y=0)

# Registration Inputs (Adjusted Y for no overlap)
tk.Label(frame2, text="Enter ID", bg="#00aeff", font=('times', 17, ' bold ')).place(x=80, y=45)
txt = tk.Entry(frame2, width=32, font=('times', 15))
txt.place(x=30, y=75)

tk.Label(frame2, text="Enter Name", bg="#00aeff", font=('times', 17, ' bold ')).place(x=80, y=120)
txt2 = tk.Entry(frame2, width=32, font=('times', 15))
txt2.place(x=30, y=150)

tk.Label(frame2, text="Enter Email", bg="#00aeff", font=('times', 17, ' bold ')).place(x=80, y=195)
txt_email = tk.Entry(frame2, width=32, font=('times', 15))
txt_email.place(x=30, y=225)

# Clear Buttons
tk.Button(frame2, text="Clear", command=clear, bg="#ea2a2a", width=11).place(x=335, y=73)
tk.Button(frame2, text="Clear", command=clear2, bg="#ea2a2a", width=11).place(x=335, y=148)
tk.Button(frame2, text="Clear", command=clear3, bg="#ea2a2a", width=11).place(x=335, y=223)

# Action Buttons
message1 = tk.Label(frame2, text="1)Take Images  >>>  2)Save Profile", bg="#00aeff", font=('times', 15, ' bold '))
message1.place(x=7, y=280)

tk.Button(frame2, text="Take Images", command=TakeImages, fg="white", bg="blue", width=34, font=('times', 15, ' bold ')).place(x=30, y=325)
tk.Button(frame2, text="Save Profile", command=TrainImages, fg="white", bg="blue", width=34, font=('times', 15, ' bold ')).place(x=30, y=395)

# Attendance Table (Left Frame)
tk.Button(frame1, text="Take Attendance", command=TrackImages, bg="yellow", width=35, font=('times', 15, ' bold ')).place(x=30, y=50)

tv = ttk.Treeview(frame1, height=13, columns=('name', 'date', 'time'))
tv.column('#0', width=82); tv.column('name', width=130); tv.column('date', width=133); tv.column('time', width=133)
tv.heading('#0', text='ID'); tv.heading('name', text='NAME'); tv.heading('date', text='DATE'); tv.heading('time', text='TIME')
tv.place(x=10, y=150)

# Clock/Date
frame3 = tk.Frame(window, bg="#262523"); frame3.place(relx=0.52, rely=0.09, relwidth=0.09, relheight=0.07)
clock = tk.Label(frame3, fg="orange", bg="#262523", font=('times', 22, ' bold '))
clock.pack()
tick()

tk.Button(frame1, text="Quit", command=window.destroy, bg="red", width=35, font=('times', 15, ' bold ')).place(x=30, y=450)

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

###################### BUTTONS ##################################

clearButton = tk.Button(frame2, text="Clear", command=clear  ,fg="black"  ,bg="#ea2a2a"  ,width=11 ,activebackground = "white" ,font=('times', 11, ' bold '))
clearButton.place(x=335, y=86)
clearButton2 = tk.Button(frame2, text="Clear", command=clear2  ,fg="black"  ,bg="#ea2a2a"  ,width=11 , activebackground = "white" ,font=('times', 11, ' bold '))
clearButton2.place(x=335, y=172)
takeImg = tk.Button(frame2, text="Take Images", command=TakeImages  ,fg="white"  ,bg="blue"  ,width=34  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
takeImg.place(x=30, y=300)
trainImg = tk.Button(frame2, text="Save Profile", command=psw ,fg="white"  ,bg="blue"  ,width=34  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
trainImg.place(x=30, y=380)
trackImg = tk.Button(frame1, text="Take Attendance", command=TrackImages  ,fg="black"  ,bg="yellow"  ,width=35  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
trackImg.place(x=30,y=50)
quitWindow = tk.Button(frame1, text="Quit", command=window.destroy  ,fg="black"  ,bg="red"  ,width=35 ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
quitWindow.place(x=30, y=450)

##################### END ######################################

window.configure(menu=menubar)
update_registration_count()
window.mainloop()

####################################################################################################
