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

**Installed modules **
Command for installation
pip install opencv-contrib-python numpy pandas Pillow 





