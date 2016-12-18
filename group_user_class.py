class GroupUser:
    def __init__(self,user_id,group_id,isAdmin, *args,**kwargs ):
        self.user_id = user_id
        self.group_id = group_id
        self.isAdmin = isAdmin
        self.user_name = kwargs.get('user_name',None)

    def json_serialize(self):
        return {
            'user_id' : self.user_id
        }