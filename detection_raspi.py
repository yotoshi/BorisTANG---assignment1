# USAGE
# python pi_face_recognition.py --cascade haarcascade_frontalface_default.xml --encodings encodings.pickle

# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import os
import subprocess
#from espeakng import ESpeakNG
import pyttsx3
from subprocess import call
import face_recognition
import argparse
import imutils
import pickle
import time
import cv2
#import speech_recognition as sr

# obtain audio from the microphone
#r = sr.Recognizer()
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--cascade", required=True,
    help = "path to where the face cascade resides")
ap.add_argument("-e", "--encodings", required=True,
    help="path to serialized db of facial encodings")

args = vars(ap.parse_args())
esng = pyttsx3.init()
#esng.voice ='english-us'
#initializing the speaker 
print("[INFO] loading encodings + face detector...")
data = pickle.loads(open(args["encodings"], "rb").read())
detector = cv2.CascadeClassifier(args["cascade"])
# load the known faces and embeddings along with OpenCV's Haar
# cascade for face detection
# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
# vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)
# loop over frames from the video file stream
while True:
    # grab the frame from the threaded video stream and resize it
    # to 500px (to speedup processing)
    frame = vs.read()
    frame = imutils.resize(frame, width=500)
    
    # convert the input frame from (1) BGR to grayscale (for face
    # detection) and (2) from BGR to RGB (for face recognition)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # detect faces in the grayscale frame
    rects = detector.detectMultiScale(gray, scaleFactor=1.1,
        minNeighbors=5, minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE)

    # OpenCV returns bounding box coordinates in (x, y, w, h) order
    # but we need them in (top, right, bottom, left) order, so we
    # need to do a bit of reordering
    boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

    # compute the facial embeddings for each face bounding box
    encodings = face_recognition.face_encodings(rgb, boxes)
    names = ["Unknown"]

    # loop over the facial embeddings
    for encoding in encodings:
        # attempt to match each face in the input image to our known
        # encodings
        matches = face_recognition.compare_faces(data["encodings"],encoding)
        name = "Unknown"

        # check to see if we have found a match
        if True in matches:
            # find the indexes of all matched faces then initialize a
            # dictionary to count the total number of times each face
            # was matched
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            # loop over the matched indexes and maintain a count for
            # each recognized face face
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1

            # determine the recognized face with the largest number
            # of votes (note: in the event of an unlikely tie Python
            # will select first entry in the dictionary)
            name = max(counts, key=counts.get)
            #print (name)        
        # update the list of names
        names.append(name)

    # loop over the recognized faces
    for ((top, right, bottom, left), name) in zip(boxes, names):
        # draw the predicted face name on the image
        cv2.rectangle(frame, (left, top), (right, bottom),
            (0, 255, 0), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
            0.75, (0, 255, 0), 2)
    # display the image to our screen
    cv2.imshow("Frame", frame)
    #time.sleep(1.0)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    name= str(names[-1])
    if names[-1] != "Unknown":
       print ("Are you "+name+"? y/n")
       #checking if the recognition is accurate
       name=name+".txt"
       key = input()
       if (key=="y"):
       #checking if there is already an existing .txt file for thisd person (default = "name.txt")
       #print(os.path.isfile(name))
           if (os.path.isfile(name)):
            print("[INFO] Would you like to edit the existing one? y/n")
            while True:
                key = input()
                if (key=="y"):
                    print("[INFO] Opening the file")
                    bashCommand = "xdg-open "+name
                    output = subprocess.check_output(['bash','-c', bashCommand])
                    break
                elif(key =="n"):
                    print("[INFO] Today, you have to take ")
                    txt = open("/home/pi/.virtualenvs/opencv/"+names[-1]+".txt","rt")
                    speechToSay=txt.read()
                    txt.close()
                    esng.say(speechToSay)
                    esng.runAndWait()
                    #reading the text file with the instruction on it
                    break
                
           else:
                print("[INFO] the file exist")
                print("[INFO] Today, you have to take ")
                txt = open("/home/pi/.virtualenvs/opencv/"+names[-1]+".txt","rt")
                speechToSay=txt.read()
                txt.close()
                esng.say(speechToSay)
                esng.runAndWait()
                #reading the text file with the instruction on it
                break
           #in case there is none textfile for the person, create one                
cv2.destroyAllWindows()
vs.stop()
