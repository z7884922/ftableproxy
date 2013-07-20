from django.http import HttpResponse, Http404
import datetime

def hello(request):
    return HttpResponse("Hello world")

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now 
    return HttpResponse(html)

#e.g. param/(\d{1,2})/, here (\d{1,2}) indicates \d{1,2} will be passed as a param. in this example, it is attached to offset.
def getparam(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt) 
    return HttpResponse(html)
