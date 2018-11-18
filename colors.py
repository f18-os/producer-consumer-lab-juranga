import socket, sys, re, os
import threading
import cv2
import time
from threading import Thread
from HelperFunctions import *

class ProducerExtractorThread(Thread):
    def __init__(self, imageQ, finished, clipFileName, vidcap):
        Thread.__init__(self, daemon=False)
        self.imageQ = imageQ
        self.clipFileName = clipFileName
        self.vidcap = vidcap
        self.finished = False
        self.start()

    def run(self):
        while not self.finished:
            self.finished = extractFrames(self.clipFileName, self.imageQ, self.vidcap)
        return

class ConsumerDisplayThread(Thread):
    def __init__(self, consumerQ,  finished):
        Thread.__init__(self, daemon=False)
        self.consumerQ = consumerQ
        self.finished = finished
        self.start()

    def run(self):
        while not self.finished:
            if not self.consumerQ.empty():
                displayFrames(self.consumerQ.get())
            else:
                time.sleep(0.0001)
        while not self.consumerQ.empty():
            displayFrames(self.consumerQ.get())
        cv2.destroyAllWindows()
        return

class ConsumerGrayScaleThread(Thread):
    def __init__(self, consumerQ, producerQ, finished):
        Thread.__init__(self, daemon=False)
        self.consumerQ = consumerQ
        self.producerQ = producerQ
        self.finished = finished
        self.start()

    def run(self):
        while not self.finished:
            if not self.consumerQ.empty():
                toGrayscale(self.consumerQ.get(), self.producerQ)
            else:
                time.sleep(0.0001)
        while not self.consumerQ.empty():
            toGrayscale(self.consumerQ.get(), self.producerQ)
        return


clipFileName = 'clip.mp4'
sharedQueue1 = queue.Queue(10)
sharedQueue2 = queue.Queue(10)
finished = True
vidcap = cv2.VideoCapture(clipFileName)


extractor = ProducerExtractorThread(sharedQueue1, finished, clipFileName, vidcap)
displayer =  ConsumerDisplayThread(sharedQueue2, finished)
grayscale = ConsumerGrayScaleThread(sharedQueue1, sharedQueue2, finished)
