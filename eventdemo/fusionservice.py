#author:xiafan68@gmail.com
#time:2013-07-18
#description: provide query service of fusion table
#
import logging
import pickle
import json
import httplib2
from eventdemo.metadata import model

from apiclient.discovery import build

from django.http import HttpResponse, Http404,HttpResponseRedirect
from google.appengine.ext import db
from google.appengine.api import memcache
from oauth2client.appengine import CredentialsProperty
from oauth2client.appengine import StorageByKeyName
from oauth2client.appengine import AppAssertionCredentials

from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import OAuth2Credentials

SCOPE='https://www.googleapis.com/auth/fusiontables'

# the client is responsible to invoke the authorization step the service is none
# when revoking service, non authorization step is triggered
# when revoking authorization, only tID is needed, client is responsible for providing tID

class FusionTabelServicePool():
    def __init__(self):
        #todo
        self.authOp2FlowMap={}
        self.authOpID=0
    

#from oauth2client.client import SignedJwtAssertionCredentials
# Here's the file you get from API Console -> Service Account.
#reference page:https://developers.google.com/api-client-library/python/guide/aaa_oauth#OAuth2WebServerFlow
    def authByFile(self):
        f = file('key.p12', 'rb')
        key = f.read()
        f.close()
        # Note that the first parameter, service_account_name,
        # is the Email address created for the Service account. It must be the email
        # address associated with the key that was created.
        credential = SignedJwtAssertionCredentials('1051573791655-2j8fighnb53na2snh7tdp5ksf9aht1c5@developer.gserviceaccount.com',
                                                    key,
                                                    scope='https://www.googleapis.com/auth/fusiontables',access_type='offline')
    #print credentials._generate_refresh_request_body()
        return credential



    def authByCode(self,request):
        tID = request.GET.get('tID')
        if not tID:
            raise Http404('argument tID should be provided')
        
        meta = model.queryTableMetaBytID(tID)
        if meta :
             return Http404('meta data for tID is not found')
        session = request.environ['beaker.session']
        session['client_id']=meta.client_id

        flow = OAuth2WebServerFlow(client_id=meta.client_id,
                                   #client_secret='0kEXw89WwZ0qpdWB2qO01_fu',
                                   client_secret=meta.client_secret,
                                   scope=SCOPE,
                                   # redirect_uri='http://localhost:8080/getcode?cid=%s&'%(client_id))
                                   #redirect_uri='http://localhost:8080/getcode'
                                   redirect_uri=meat.redirect_uri)
        auth_uri = flow.step1_get_authorize_url()
        session = request.environ['beaker.session']
        session['flow']=pickle.dumps(flow)
        return HttpResponseRedirect(auth_uri)

    def getCred(self, client_id):
        #client_id = '1051573791655-s4ib8bfpibhk5i9o5vnnto0ldvutaadt.apps.googleusercontent.com'
        #credential = StorageByKeyName(Credentials, client_id, 'credentials').get()
        credRec = Credentials.all().filter('client_id = ', client_id).get()
        if credRec :
            return credRec.credential
        else: 
            logging.info("credential is not stored in the storage")
            return None

    def authByApp(self):
        return AppAssertionCredentials(scope='https://www.googleapis.com/auth/fusiontables')

    def refreshToken(self, client_id, credential):
        credential.refresh(httplib2.Http())
        credRec = Credentials(client_id=client_id,credential=credential)
        credRec.put()

    def newService(self, tID):
        # Create an httplib2.Http object to handle our HTTP requests 
        # and authorize it with the Credentials
        # TODO from tID to client_id
        #client_id = '1051573791655-s4ib8bfpibhk5i9o5vnnto0ldvutaadt.apps.googleusercontent.com'
        client_id= model.getClientID(tID)
        if client_id is None:
            return None

        credential = self.getCred(client_id)
        if credential :
            service = None
            loop = 0
            while service is None and loop < 2:
                loop += 1
                http = httplib2.Http()
                http = credential.authorize(http)
                try:
                    service = build("fusiontables", "v1", http=http) 
                except Exception:
                    self.refreshToken(client_id, credential)

            return service
        else:
            #raise Http404()
            return None

    def validToken(self, request):
        code =request.GET.get('code')
        session = request.environ['beaker.session']
        #client_id = '1051573791655-s4ib8bfpibhk5i9o5vnnto0ldvutaadt.apps.googleusercontent.com'
        client_id = session['client_id']
        del session['client_id']

        if session.get('flow') :
            flow = pickle.loads(session['flow'])
            del session['flow']
            if flow :
                credential = flow.step2_exchange(code)
                logging.error(str(credential))
                #StorageByKeyName(Credentials, client_id, 'credentials').put(credentials)
                credRec = Credentials(client_id=client_id,credential=credential)
                credRec.put()
                #del self.authOp2FlowMap[client_id]
                return HttpResponse("auth success")
            else:
                return HttpResponse("no flow auth fail")
        else:
            return HttpResponse("no authOpID auth fail")

    def service(self,tID):
        # todo
        return self.newService(tID)


ftServicePool = FusionTabelServicePool()


def authStepInit(request):
    global ftServicePool
    #client_id='1051573791655-s4ib8bfpibhk5i9o5vnnto0ldvutaadt.apps.googleusercontent.com'
    #if ftServicePool.newService(request,'') is None :
    return ftServicePool.authByCode(request)

def AuthStepValidToken(request):
    global ftServicePool
    #session = request.environ['beaker.session']
    return ftServicePool.validToken(request)
 

count=1    
def testGlobalState(request):
    global count
    count= count + 1
    global ftServicePool
    client_id='1051573791655-s4ib8bfpibhk5i9o5vnnto0ldvutaadt.apps.googleusercontent.com'
    if ftServicePool.newService('') is None :
        return ftServicePool.authByCode(request, client_id)
    return HttpResponse(count)

