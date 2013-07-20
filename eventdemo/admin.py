# author:xiafan68@gmail.com
# time:2013-07-18
# description: provide administration for all meta data
#

#
# service for:
# 1. adding table meta data 
# 2. adding partition meta data for a key of a table, e.g. eventName of event table
# 
#
#
from metadata import model
from django.http import Http404,HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context

def parseTableSelRange(request):
    tMetaStarts = request.GET.get('tms')
    start = 0
    if tMetaStarts :
        start = int(tMetaStarts)    
    
    limits = request.GET.get('tml')
    limit = 10
    if limits :
        limit = int(limits)
    return (limit, start)

def adminPage(request):
    tableRange = parseTableSelRange(request)
    tableMetas = model.selectAllTableMeta(tableRange[0], tableRange[1])
    isAutheds = []
    for tableMeta in tableMetas :
        isAutheds.append(model.isClientHasAuthed(tableMeta.client_id))
    
    tMetaCount = len(tableMetas)
    t = get_template('admin.html')
    c = Context({'tableMetas':tableMetas, 'tMetaCount':tMetaCount,
                 'isAutheds':isAutheds})
    return HttpResponse(t.render(c))

def processAdminCmd(request):
    # input: 
    #
    cmd = request.GET.get('cmd')
    if cmd == 'insertTableMeta':
        return setTableMetaData(request)
    else :
       raise Http404("command %s not found"%(cmd))

def setTableMetaData(request):
    tID = request.GET.get('tID')
    client_id = request.GET.get('secret')
    secret = request.GET.get('secret')
    redirect_uri= request.GET.get('redirect_uri')
    model.insertTableMetaData(tID, client_id, secret, redirect_uri)
    return HttpResponseRedirect("/admin/index.html")


