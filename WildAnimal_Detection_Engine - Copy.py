import numpy as np
import cv2
import os
import os
import cv2
import numpy as np
import sys
import glob
import random
import importlib.util
from tensorflow.lite.python.interpreter import Interpreter
import operator
import collections
import matplotlib.pyplot as plt
from mutagen.mp3 import MP3
from gtts import gTTS
import matplotlib
import pyglet
import os, time
import threading
import collections
import datetime
import operator
from pygame import mixer   
modelpath="model/detect.tflite"
lblpath='model/labelmap.txt'
min_conf=0.5
txt_only=False
def playvoice(typename):
    audiofilename=""
    if(typename=="Leopard"):
        print("Got leopard")
        audiofilename="Audio_Files/leopard_warning_audio.MPEG"
    elif(typename=="Elephant"):
        audiofilename="Audio_Files/elephant_warning_audio.MPEG"
    elif(typename=="Tiger"):
        audiofilename="Audio_Files/tiger_warning_audio.MPEG"   
        
    mixer.init()
    mixer.music.load(audiofilename)
    mixer.music.play()
    while mixer.music.get_busy():
        time.sleep(1)  
with open(lblpath, 'r') as f:
    labels = [line.strip() for line in f.readlines()]
# Load the Tensorflow Lite model into memory
interpreter = Interpreter(model_path=modelpath)
interpreter.allocate_tensors()
# Get model details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]
float_input = (input_details[0]['dtype'] == np.float32)
input_mean = 127.5
input_std = 127.5            
cap=cv2.VideoCapture(1)
count=0
xmin=1
xmax=450
current,previous=0,0
resultlist=[]
imageno=1
while cap.isOpened():
    _,capimg=cap.read()
    image_rgb = cv2.cvtColor(capimg, cv2.COLOR_BGR2RGB)
    imH, imW, _ = capimg.shape
    image_resized = cv2.resize(image_rgb, (width, height))
    input_data = np.expand_dims(image_resized, axis=0)

    # Normalize pixel values if using a floating model (i.e. if model is non-quantized)
    if float_input:
        input_data = (np.float32(input_data) - input_mean) / input_std

    # Perform the actual detection by running the model with the image as input
    interpreter.set_tensor(input_details[0]['index'],input_data)
    interpreter.invoke()

    # Retrieve detection results
    boxes = interpreter.get_tensor(output_details[1]['index'])[0] # Bounding box coordinates of detected objects
    classes = interpreter.get_tensor(output_details[3]['index'])[0] # Class index of detected objects
    scores = interpreter.get_tensor(output_details[0]['index'])[0] # Confidence of detected objects

    detections = []
    for i in range(len(scores)):
        if ((scores[i] > min_conf) and (scores[i] <= 1.0)):

            # Get bounding box coordinates and draw box
            # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
            ymin = int(max(1,(boxes[i][0] * imH)))
            xmin = int(max(1,(boxes[i][1] * imW)))
            ymax = int(min(imH,(boxes[i][2] * imH)))
            xmax = int(min(imW,(boxes[i][3] * imW)))
           # current=xmin
           # print("C : ",current)
            # Draw label
            object_name = labels[int(classes[i])] # Look up object name from "labels" array using class index
            finscore=int(scores[i]*100)
            if(finscore>=99):
                cv2.rectangle(capimg, (xmin,ymin), (xmax,ymax), (10, 255, 0), 2)
                               
                label = '%s: %d%%' % (object_name, int(scores[i]*100)) # Example: 'person: 72%'
                labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2) # Get font size
                label_ymin = max(ymin, labelSize[1] + 10) # Make sure not to draw label too close to top of window
                cv2.rectangle(capimg, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED) # Draw white box to put label text in
                cv2.putText(capimg, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2) # Draw label text
    
                detections.append([object_name, scores[i], xmin, ymin, xmax, ymax])
                print("Animal is ",object_name)
                resultlist.append(object_name)
                frequency = collections.Counter(resultlist)
                cropfreq=dict(frequency)
                sorted_d = sorted(cropfreq.items(), key=operator.itemgetter(1))
               # print('Dictionary in ascending order by value : ',sorted_d)
                index=len(sorted_d)-1
                mxvaluecrop=sorted_d[index] 
                
                print("Matched ",mxvaluecrop)
                typename=mxvaluecrop[0]
                typecount=mxvaluecrop[1]
 
                # print("typename ",typename)
               # print("HHHH ",type(typename))
                print("typecount ",typecount)
                count=int(typecount) 
                print("Count === ",count)
                
                if(count>=3):
                    print("Entered ============")
                    imagepath="Captured_images//"+str(imageno)+".jpg"
                    imageno=imageno+1 
                    
                    cv2.imwrite(imagepath, capimg)
                    if(typename=="Leopard"):
                        print("Leopard Detected")
                        t1 = threading.Thread(target=playvoice, args=(typename,))
                        t1.start()
                        import Shooting
                        Shooting.startShooting()
                        import WhatsAppSender
                        WhatsAppSender.sendInfoWA(imagepath, typename)
                    
                        resultlist.clear()
                    if(typename=="Tiger"):
                        print("Tiger Detected")
                        t1 = threading.Thread(target=playvoice, args=(typename,))
                        t1.start()
                        import Shooting
                        Shooting.startShooting()
                        import WhatsAppSender
                        WhatsAppSender.sendInfoWA(imagepath, typename)
                    
                        resultlist.clear()
                    if(typename=="Elephant"):
                        print("Elphant Detected")
                        t1 = threading.Thread(target=playvoice, args=(typename,))
                        t1.start()
                        import Shooting
                        Shooting.startShooting()
                        import WhatsAppSender
                        WhatsAppSender.sendInfoWA(imagepath, typename)
                   
                        resultlist.clear()
                
                #
                         
    
    cv2.imshow('Capture Image( Press q to quit)',capimg)
    
    if cv2.waitKey(1)==ord('q'):
        break
       
      
                
          


cap.release()
cv2.destroyAllWindows()