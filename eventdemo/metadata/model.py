# author:xiafan68@gmail.com
# time:2013-07-18
# description: data model
#
from google.appengine.ext import db
from oauth2client.appengine import CredentialsProperty

class LogicTableMeta(db.Model):
    logicTableName=db.StringProperty(required=True)
    fTableID=db.StringProperty(required=True)

def selLogicTableMetaByLTName(logicTableName, start, limit):
    records=LogicTableMeta.all().filter('logicTableName=',logicTableName) \
        .fetch(limit, offset=start)
    return records

def insertLogicTableMeta(lTableName, fTableID):
    rec = LogicTableMeta(logicTableName=lTableName, fTableID=fTableID)
    rec.put()

def delLogicTableMeta(lTableName, fTableID):
    rec = LogicTableMeta.all().filter('logicTableName=',lTableName) \
        .filter('fTableID=',fTableID).get()
    rec.delete()

class Credentials(db.Model):
    client_id=db.StringProperty(required=True)
    credential = CredentialsProperty(required=True)

def isClientHasAuthed(client_id):
    rec = Credentials.all().filter('client_id = ', client_id).get()
    if rec :
        return True
    else:
        return False

# record information about a fusion table
class TableMetaData(db.Model):
    tID=db.StringProperty(required=True)
    client_id=db.StringProperty(required=True, indexed=False)
    secret=db.StringProperty(required=True, indexed=False)
    redirect_uri=db.StringProperty(required=True, indexed=False)

def getClientID(tID):
    meta = TableMetaData.all().filter('tID=', tID).get()
    if meta :
        return meta.client_id
    else :
        return None

def insertTableMetaData(tID, client_id, secret, redirect_uri):
    meta=TableMetaData(tID=tID,client_id=client_id, 
                       secret=secret, redirect_uri=redirect_uri)
    meta.put()
    # TODO cache is necessary

def selectAllTableMeta(start, limit):
    return TableMetaData.all().fetch(start, limit)

def queryTableMetaBytID(tID):
    #considing cache
    q=TableMetaData.all()
    meta = q.filter('tID=', tID).get()
    return meta


#each tuple records each key's partition info
class PartTableTuple(db.Model):
    tableName = db.StringProperty(required=True)
    pKey=db.StringProperty(required=True)
    tID=db.StringProperty(required=True)


