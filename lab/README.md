# Producer Consumer Lab

In this lab, we were required to run three concurrent threads that convert frames to grayscale before displaying them to the user in a video format.

## Files located within:

#### HelperFunctions.py
* In this file, three methods can be found that are used in the lab.py class
    1) toGrayscale()
    - This method converts the frame that it receives in to grayscale and adds this grayscaled image to a queue.

    2) extractFrames()
    - This method extracts the frames from a video file and adds them to a queue. 

    3) displayFrames()
    - This method displays the grayscaled images from the Grayscale queue.

#### Lab.py
* In this file, you will find three classes which use the methods found in HelperFunctions.py
    1) ProducerExtractorThread
    - This class creates a thread for the extractFrames method

    2) ConsumerDisplayThread
    - This class creates a thread for the displayFrames method

    3) ConsumerGrayScaleThread
    - This class creates a thread for the toGrayScale method

# Running the lab:
To run:

    `python3 lab.py`
