#!/bin/sh

#Install packages

#PACKAGES = dlib
#apt-get update
#apt-get upgrade -y
#pip install dlib

#PACKAGES = face_recognition
#pip install face_recognition

#PACKAGES = imutils
#pip install imutils

#PACKAGES = pyttsx3
#pip install pyttsx3

#ENABLE Camera interface~
#CONFIG = /boot/config.txt
grep "start_x=1" /boot/config.txt
if grep "start_x=1" /boot/config.txt
then
        exit
else
        sed -i "s/start_x=0/start_x=1/g" /boot/config.txt
        reboot
fi
exit
