from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from appcam.camera import *



@gzip.gzip_page
def livefeed(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad!
        pass

def index(request, *args, **kwargs):
    return render(request, 'index.html')
