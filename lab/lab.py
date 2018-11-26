import socket, sys, re, os
import threading
import cv2
from queue import Q
import time
from threading import Thread, Lock
from HelperFunctions import *

# Creates Thread that Extracts video frames and feeds them to a Queue shared with Greyscale Thread
class ProducerExtractorThread(Thread):
    imageQ = None
    vidcap = cv2.VideoCapture('clip.mp4')

    def __init__(self, imageQ):
        Thread.__init__(self, daemon=False)
        ProducerExtractorThread.imageQ = imageQ
        self.start()

    def run(self):
        global finished
        finished = extractFrames(ProducerExtractorThread.imageQ, ProducerExtractorThread.vidcap, success=True)
        return

class ConsumerDisplayThread(Thread):
    consumerQ = None

    def __init__(self, consumerQ):
        Thread.__init__(self, daemon=False)
        ConsumerDisplayThread.consumerQ = consumerQ
        self.start()

    def run(self):
        global finished2
        while not finished2:
            if not ConsumerDisplayThread.consumerQ.empty():
                displayFrames(ConsumerDisplayThread.consumerQ.get())
            else:
                time.sleep(0.0001)
        while not ConsumerDisplayThread.consumerQ.empty():
            displayFrames(ConsumerDisplayThread.consumerQ.get())
        cv2.destroyAllWindows()
        return

# Creates GrayScale Consumer Thread that contains both a Consumer and Producer Queue
# Consumer Queue gets frame data from Extractor Queue 
# Producer Queue is the queue that is fed after the images are turned greyscale
class ConsumerGrayScaleThread(Thread):
    consumerQ = None 
    producerQ = None 

    def __init__(self, consumerQ, producerQ):
        Thread.__init__(self, daemon=False)
        ConsumerGrayScaleThread.consumerQ = consumerQ
        ConsumerGrayScaleThread.producerQ = producerQ
        self.start()

    def run(self):
        global finished; global finished2
        while not finished:
            if not ConsumerGrayScaleThread.consumerQ.empty():
                toGrayscale(ConsumerGrayScaleThread.consumerQ.get(), ConsumerGrayScaleThread.producerQ)
            else:
                time.sleep(0.0001)
        while not ConsumerGrayScaleThread.consumerQ.empty():
            toGrayscale(ConsumerGrayScaleThread.consumerQ.get(), ConsumerGrayScaleThread.producerQ)
        finished2 = True
        return

global finished; global finished2
lock = Lock()
lock2 = Lock()
sharedQueue1 = Q(10, lock)
sharedQueue2 = Q(10, lock2)
finished = False; finished2 = False
extractor = ProducerExtractorThread(sharedQueue1)
displayer =  ConsumerDisplayThread(sharedQueue2)
grayscale = ConsumerGrayScaleThread(sharedQueue1, sharedQueue2)
