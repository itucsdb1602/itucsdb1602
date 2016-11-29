class Group:
    def __init__(self,name,id = 0):
        self.id = id
        self.name = name

    def json_serialize(self):
        return {
            'id' : self.id,
            'name' : self.name
        }