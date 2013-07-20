#author: xiafan68@gmail.com
#description:
#as it is possible that each table will be stored in multiple fusion tables, it is 
#necessary to store the partitions meta data in the system.
#
#each tuple in a table will be partitioned by a key of the tuple
#in this implementation, we use a table to record for each key which partition it is stored.
#
from google.appengine.ext import db
from eventdemo.metadata.model import TableMetaData,PartTableTuple

class LookupTable:
    def __init__(self):
      tName2TIDsMap={}
      tNamePartMap={} #mappings from table name to table partition meta data, which is another map
      partMetas={}

    def lookup(self,table, key):
        if (not tNamePartMap.get(table)) or (not tNamePartMap.get(table).get(key)) :
            self.loadMeta(table,key)
            #reading from backends?
        return tNamePartMap[table][key]

    def loadMeta(self,table, key):
        q = db.Query(PartTableTuple)
        q.filter('tableName = ', table).filter('pKey = ', key)
        meta = q.get() #q.fetch(10, offset=10) returns a list
        if meta:
            tNamePartMap[meta.tableName]={meta.pKey: meta.tID}
        else:
            raise Exception("partition meta data for %s.%s does not exist"%(table, key))

    def delMeta(self,table, key):
        q = db.Query(PartTableTuple)
        q.filter('tableName = ', table).filter('pKey = ', key)
        meta = q.get() #q.fetch(10, offset=10) returns a list
        if meta:
           meta.delete()

    #if flush == true, also delete the meta in the database, can be used
    #when the client find the meta is abnormal
    def delPartition(self,table, key, flush):
        tableMeta = tNamePartMap.get(table)
        if tableMeta :
            del tableMeta[key]
        if flush :
           self.delMeta(table, key)
    
    def addMeta(self,table, key, tID):
        obj= PartTableTuple(table, key, tID)
        obj.put()

    def getPartMeta(self,tID):
        #TODO
        if not partMetas.get(tID):
            meta = model.queryTableMetaBytID(tID) 
            #q=PartMetaTuple.all()
            #meta = q.filter('tID=', tID).get()
            if meta :
                partMetas[tID]=meta
        return partMetas.get(tID)

lookupTable = LookupTable() #skeleton; seems no means in web context?
