from lookuptable import lookupTable
from django.http import HttpResponse
import json

#possible operation:
#add
#get
#del
def lookupService(request):
    op = request.GET.get('op')
    tableName = request.GET.get('tName')
    key = request.GET.get('key')
    ret={"status":"ok"}
    try:
        if op == 'get':
            ret['reply']= lookupTable.lookup(table, key)
        elif op == 'del':
            partition.delMeta(table, key)
        elif op == 'add':
            tID = request.GET.get('tID')
            if tId :
                lookup.addMeta(table, key, tID)
            else:
                ret['status']='error'
                ret['error']="tID is not provided"
        else:
             ret['status']='error'
             ret['error']="op is not provided"
    except Exception,e:
        ret['status']='error'
        ret['error']=str(e)
    return HttpResponse(json.dumps(ret))
