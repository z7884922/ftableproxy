#parse the arguments in datasource protocol request
TQX_FIELD='tqx'
TQX_REQID_FIELD='reqId'

RESP_TABLE_FIELD='table'
RESP_REQID_FIELD='reqId'
RESP_STATUS_FIELD='status'
RESP_ERROR_FIELD='errors'
RESP_WARNING_FIELD='warnings'
RESP_SIG_FIELD='sig'
RESP_VERSION_FIELD='version'
TQ_FIELD='tq'

def parseReqArgs(request):
    argsMap = {}
    tqx = request.GET.get(TQX_FIELD)
    if tqx :
        #possible args:
        #regId[+]: the request id, must returned as part of the response
        #version[?]
        #sig[?]: the hash signature of previous request, used for optimization to avoid data transformation
        #out[?] sepecify the kind of output such as json,html, csv,tsv-excel
        tqxMap={}
        tqxArgs = tqx.split(';')
        for argStr in tqxArgs:
            argArr = argStr.split(':')
            if len(argArr) == 2:
                tqxMap[argArr[0]]=argArr[1]
        argsMap[TQX_FIELD]=tqxMap
    tq = request.GET.get(TQ_FIELD)
    if tq :
        argsMap[TQ_FIELD]=tq
    return argsMap

def addWarning(warnings, reason, message):
    warnings.add(buildWarning(reason, message))

def buildWarning(reason, message):
    return {"reason":reason, 'message':message}

def buildResp(reqId, version=None, status='OK', warnings=None, errors=None, sig=None, table=None):
    resp={}
    resp[RESP_REQID_FIELD]=reqId
    resp[RESP_STATUS_FIELD]=status
    if table :
        resp[RESP_TABLE_FIELD]=table
    if version :
        resp[RESP_VERSION_FIELD]=version
    if warnings :
        resp[RESP_WARNING_FIELD] = warnings
    if errors :
        resp[RESP_ERROR_FIELD] = errors
    if sig :
        resp[RESP_SIG_FIELD] = sig
    return resp
