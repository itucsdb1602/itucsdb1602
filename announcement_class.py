from datetime import date
class Announcement:
    def __init__(self,name,fromuserid,fromgroupid,date = None,id = 0,fromuser = None):
        self.id = id
        self.name = name
        self.fromuser = fromuser
        self.fromgroupid = fromgroupid
        self.fromuserid = fromuserid
        self.date = date
    def json_serialize(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'fromgroupid' : self.fromgroupid
        }