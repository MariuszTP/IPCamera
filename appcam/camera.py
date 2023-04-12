import cv2
import os
#import imutils
#from imutils.video import VideoStream
from django.http import StreamingHttpResponse
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import threading


#RTSP_URL = "rtsp://admin:admin@192.168.1.117/2/"

RTSP_URL = "rtsp://109.173.166.155/2/ "
os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] ='rtsp_transport;udp' # Use tcp instead of udp if stream is unstable
cap = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG)

class VideoCamera(object):
    def __init__(self):
        self.video = cap
        (self.grabbed, self.frame) = cap.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        #image = imutils.resize(image, width = 1600)
        #image = cv2.resize(image, None, fx = 2, fy = 2)
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')



