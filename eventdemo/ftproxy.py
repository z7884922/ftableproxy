#
#
# TODO: define the query interface
# 1. just redirect the sql to proper fusion table
# 2. provide a new query protocol
#
import logging

import httplib2
import json
import random
from dsprotocol import *
#from datetime import datetime
#from datetime import date
from django.http import HttpResponse, Http404
from fusionservice import ftServicePool

#from time import time,sleep,clock

def execSQL (sql):
    #for i in range(10):
    #   start = clock()
    #   ret=service.query().sql(sql=sql).execute()
        #print(ret['columns'])
        #print(ret['rows'])
    #   print(len(ret['rows']))
    #   end = clock()
    #   print "time cost for retrieval: %f s"%((end - start))
    service=ftServicePool.service("")
    return service.query().sql(sql=sql).execute()

# For example, let make SQL query to SELECT ALL from Table with
# id = 1gvB3SedL89vG5r1128nUN5ICyyw7Wio5g1w1mbk
#print(service.table().list().execute())

#TODO define the query interface
def ftproxy(request):
    argsMap = parseReqArgs(request)
    data = execSQL(argsMap[TQ_FIELD])
    # data={'cols': [{'id': 'A', 'label': 'NEW A', 'type': 'string'},
    #              {'id': 'B', 'label': 'B-label', 'type': 'number'}],
    #     'rows': [{'c': [{'v': 'a'}, {'v': 1.0, 'f': 'One'}]},
    #             {'c':[{'v': 'b'}, {'v': 2.0, 'f': 'Two'}]},
    #            {'c':[{'v': 'c'}, {'v': 3.0, 'f': 'Three'}]}
    #           ]}
    ret= buildResp(reqId=argsMap[TQX_FIELD][TQX_REQID_FIELD], table=data)
    return HttpResponse(json.dumps(ret))

if __name__ == '__main__':
    frproxy()
