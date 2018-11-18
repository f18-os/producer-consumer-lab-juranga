#!/usr/bin/env python3

import cv2
import threading
import numpy as np
import base64
import time
import queue

def toGrayscale(inputFrame=None, outputBuffer=None):
    while inputFrame is not None:
        # convert the image to grayscale
        grayscaleFrame = cv2.cvtColor(inputFrame, cv2.COLOR_BGR2GRAY)
        # add to grayscale queue
        outputBuffer.put(grayscaleFrame)

        while outputBuffer.full():
            time.sleep(0.0001)

def extractFrames(fileName, outputBuffer, vidcap, success=True):
    while success:
        success,image = vidcap.read()
        if not success:
            break
        # get a jpg encoded frame
        success, jpgImage = cv2.imencode('.jpg', image)
        #encode the frame as base 64 to make debugging easier
        jpgAsText = base64.b64encode(jpgImage)
        # add the frame to the buffer
        outputBuffer.put(jpgAsText)

        while outputBuffer.full():
            time.sleep(0.0001)

    return True
    
def displayFrames(inputFrame):
    while inputFrame is not None:
        # decode the frame 
        jpgRawImage = base64.b64decode(inputFrame)
        # convert the raw frame to a numpy array
        jpgImage = np.asarray(bytearray(jpgRawImage), dtype=np.uint8)
        # get a jpg encoded frame
        img = cv2.imdecode( jpgImage ,cv2.IMREAD_UNCHANGED)   

        # display the image in a window called "video" and wait 42ms
        # before displaying the next frame
        cv2.imshow("Video", img)
        if cv2.waitKey(42) and 0xFF == ord("q"):
            break
    
