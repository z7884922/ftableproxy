# author:xiafan68@gmail.com
# time:2013-07-28
# description: provide administration web interface to manage the model
#
from django.http import HttpResponse, Http404
from eventDemo.metadata import modelview
from eventDemo import util

def logicTableMetaView(request):
    action = request.GET.get("action")
    ltName = util.getRequestArg(request, 'ltName', '')
    if action == "insert":
        #TODO:
       tTableID = util.getRequestArg(request,'fTableID', '')
       model.insertLogicTableMeta(ltName, tTableID)

    elif action = "sel":
        start = util.getRequestArg(request,'start', 0)
        limit = util.getRequestArg(request, 'limit', 10)
        model.selLogicTableMetaByLTName(ltName, start, limit)
        
    elif action = "del":
        tTableID = util.getRequestArg(request,'fTableID', '')
        model.delLogicTableMeta(ltName, tTableID)

def credentialView(request):
    action = request.GET.get("action")
    if action == "insert":
        #TODO:
        elif action = "sel":
        elif action = "del":

def tableMetaDataView(request):
    action = request.GET.get("action")
    if action == "insert":
        #TODO:
        elif action = "sel":
        elif action = "del":


def PartTableTupleView(request):
    action = request.GET.get("action")
    if action == "insert":
        #TODO:
        elif action = "sel":
        elif action = "del":
