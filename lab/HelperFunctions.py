#!/usr/bin/env python3
import cv2
import threading
import numpy as np
import base64
import time
from queue import Queue

def toGrayscale(inputFrame=None, outputBuffer=None):
    if inputFrame is not None:
        grayscaleFrame = cv2.cvtColor(inputFrame, cv2.COLOR_BGR2GRAY)
        outputBuffer.put(grayscaleFrame)
        while outputBuffer.full():
            time.sleep(0.0001)

def extractFrames(fileName, outputBuffer, vidcap, success=True):
    while success:
        success,image = vidcap.read()
        outputBuffer.put(image)
        while outputBuffer.full():
            time.sleep(0.0001)
    return True
    
def displayFrames(inputFrame):
    if inputFrame is not None:
        img = inputFrame 
        cv2.imshow("Video", img)
        cv2.waitKey(42)
