import cv2
import os
import numpy
datasetpath="Wild_Animal_Dataset123"
if not os.path.exists(datasetpath):
    os.makedirs(datasetpath)        
cap=cv2.VideoCapture(1)
imgeno=1
while cap.isOpened():
    _,capimg=cap.read()
    cv2.imshow('Wild Animal Dataset Creator Image( Press q to quit)',capimg)
    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
    # SPACE pressed
        filename=str(imgeno)   
        newfilepath=datasetpath+"//"+filename+".jpg"      
        cv2.imwrite(newfilepath,capimg)
        imgeno=imgeno+1
        print("Image path is ",newfilepath)
  
                
          


cap.release()
cv2.destroyAllWindows()