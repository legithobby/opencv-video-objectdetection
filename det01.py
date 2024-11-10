import cv2
import numpy as np
import os
import sys
from datetime import datetime, time
import time as timetime
from detopencvmodule import GetCoords as Gc
from detopencvmodule import OncePerInterval as Opi
import threading
from dotenv import load_dotenv

def mylog(messa):
        filename = './debug.log'
        with open(filename, 'a') as mylogfile:
            timestamp = datetime.now().isoformat(sep=' ', timespec='milliseconds')
            mylogfile.write(timestamp + " " + messa + '\n')

def imgsavetodisk(capimg, fipath, fiprefix):
    timestamp = str(datetime.now().strftime("%Y%m%d-%H%M%S-%f"))
    filename = os.path.join(fipath, "{}_{}.jpg".format(fiprefix, timestamp))
    cv2.imwrite(filename, capimg)
    
def push():
      mylog("Starting push")
      os.system('./push.sh &')
      timetime.sleep(8)

def recaudio():
      mylog("Starting audio recording")
      os.system('./recaudio &')
      timetime.sleep(20)
      
def savetestimg():
  ret, testimg = cap.read()
  imgsavetodisk(testimg, './img/', "testimg")
  cro = testimg[y1:y2, xle1:xri2]
  imgsavetodisk(cro, './img/', "test")
  exit()

if __name__ == "__main__":
  # Read camera credentials and connection details from .env
  load_dotenv('./.env')
  CAM_USERNAME = os.getenv('CAM_USERNAME')
  CAM_PASSWORD = os.getenv('CAM_PASSWORD')
  CAM_IP = os.getenv('CAM_IP')
  CAM_PORT = os.getenv('CAM_PORT')
  
  RTSP_STREAM_URL = f"rtsp://{CAM_USERNAME}:{CAM_PASSWORD}@{CAM_IP}:{CAM_PORT}/videoSub"

  # Define the minimum and maximum area of a detected motion region
  MIN_AREA = 150
  MAX_AREA = 1000
    
  # Initialize the background subtractor
  background_subtractor = cv2.createBackgroundSubtractorMOG2()
  
  # Initialize the reference frame
  reference_frame = None
  
  # Capture the RTSP stream
  cap = cv2.VideoCapture(RTSP_STREAM_URL)
  
  mylog("Started det01.py")
  
  opi_push = Opi.OncePerInt(push)
  opi_record = Opi.OncePerInt(recaudio)
  	
  frame_counter = 0
  lastlogtime = 0.0
  
  y1, y2, xle1, xle2, xmi1, xmi2, xri1, xri2 = Gc.getcoords()
  
  if sys.argv[1] == "testimg":
    savetestimg()
  
  # Loop over the video stream
  while True:
  
      # to read frame by frame
      ret, img_1 = cap.read()
  
      if not ret:
          nowtime = timetime.time()
          if nowtime - lastlogtime > 50.0:
              #print(nowtime - lastlogtime)
              lastlogtime = nowtime
              mylog("Could not read image")
          continue    
  
      now_time = datetime.now().time()
      if now_time > time(7, 30, 00, 00) and now_time < time(14, 10, 00, 00):
          mylog("Daytime, exiting")
          exit()
  
      cro_left = img_1[y1:y2, xle1:xle2]
      cro_mid = img_1[y1:y2, xmi1:xmi2]
      cro_right = img_1[y1:y2, xri1:xri2]
  
      gray_cro_left = cv2.cvtColor(cro_left, cv2.COLOR_BGR2GRAY)
      gray_cro_mid = cv2.cvtColor(cro_mid, cv2.COLOR_BGR2GRAY)
      gray_cro_right = cv2.cvtColor(cro_right, cv2.COLOR_BGR2GRAY)        
  
      ave_br_left = int(gray_cro_left.mean())
      ave_br_mid = int(gray_cro_mid.mean())
      ave_br_right = int(gray_cro_right.mean())
      
  
      if ( ave_br_mid < ave_br_left - 9 or ave_br_mid < ave_br_right - 9 ) and ave_br_left < 115 and ave_br_right < 115	 :    
          mylog("Average brightnesses " + str(ave_br_left) + " " + str(ave_br_mid) + " " + str(ave_br_right) )
          imgsavetodisk(img_1, './img/', "motdet")
          opi_push.runcmd()
          mylog("det01.py object detected")
  
      # Increment the frame counter
      frame_counter += 1
  
  # Release the capture device
  cap.release()
  
  
