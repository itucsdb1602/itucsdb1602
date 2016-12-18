class Keywords:
    def __init__(self,name,tag_id,*args, **kwargs):
        self.id = kwargs.get('id',None)
        self.name = name
        self.tag_id = tag_id
        self.tag_name = kwargs.get('tag_name',None)

    def json_serialize(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'tag_id': self.tag_id,
            'tag_name': self.tag_name
        }