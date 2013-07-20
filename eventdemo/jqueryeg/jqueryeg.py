from django.template.context import RequestContext
from django.shortcuts import render_to_response
import json
from django.http import HttpResponse
from eventdemo import settings
import logging

def jsonp(request):
    callback = request.GET.get('callback')
    start = request.GET.get('start')
    if start is None:
        start = 0
    limit = request.GET.get('limit')
    if limit is None:
        limit = 0
    
    resp = {"hits": 1,
            "request": 
            {"start": int(start), "limit": int(limit),
             "weights": {"client_id":1.0,"secret":1.0,"tID":1.0,"redirect_uri":1.0},
             "filter": {"fields": {"type": ["submission"]}, "queries": []}}, 
             "results": [{"client_id":'1',"secret":"1","tID":"1","redirect_uri":"a"}]}
    respj=json.dumps(resp)
    resps='%s(%s);'%(callback, str(resp))
    logging.error(resps)
    response = HttpResponse(resps)
    response['Content-Type'] = "text/javascript" 
    return response
def jqueryEg(request):
    template = 'jqueryeg.html'

    app_action = request.POST.get('app_action')
    posted_data = request.POST.get('json_data')
    callback = request.GET.get('callback')
    logging.error("callback is %s"%(callback))
    if callback :
        return jsonp(request)
    elif posted_data is not None and app_action == 'save':
        this_sheet = request.POST.get("sheet")
        this_workbook = request.POST.get("workbook_name")
        sheet_id = request.POST.get("sheet_id")

        posted_data = json.dumps(posted_data)

    elif app_action == 'get_sheets':
        #query the backend

        # use list comprehension to create python list which is like a JSON object
        sheets={'tID':'data','client_id':'s','secret':'s','redirect_uri':'s'}
        # dumps -> serialize to JSON
        sheets = json.dumps(sheets)

        return HttpResponse( sheets, mimetype='application/javascript' )

  

        # We need to return an HttpResponse object in order to complete
        # the ajax call
        return HttpResponse("", mimetype='application/javascript' )
    logging.debug('MEDIA_URL:%s'%(settings.MEDIA_URL))
    return render_to_response(template, {'MEDIA_URL': settings.MEDIA_URL},
           context_instance = RequestContext( request ))
