class Complaint:
    #Complaint class which takes the user id
    def __init__(self,complaint_text,complaint_object,complaint_object_id,crt_id,*args,**kwargs):
        self.id = kwargs.get('id',None)
        self.complaint_text = complaint_text
        self.complaint_object = complaint_object
        self.complaint_object_id = complaint_object_id
        self.crt_id = crt_id
        self.crt_time = kwargs.get('crt_time',None)
        self.upd_id = kwargs.get('upd_id',None)
        self.upd_time = kwargs.get('upd_time',None)
        self.crt_username = kwargs.get('crt_username',None)
        self.upd_username = kwargs.get('upd_username',None)
        self.is_done = kwargs.get('is_done',None)

    def json_serialize(self):
        return {
            'id' : self.id,
            'complaint_text' : self.complaint_text,
            'complaint_object': self.complaint_object,
            'complaint_object_id':self.complaint_object_id,
            'crt_id': self.crt_id,
            'crt_time': self.crt_time,
            'upd_id': self.upd_id,
            'upd_time': self.upd_time,
            'crt_username': self.crt_username,
            'upd_username': self.upd_username,
            'is_done': self.is_done
        }
