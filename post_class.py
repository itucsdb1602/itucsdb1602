class Post:
    def __init__(self,post_text,tag_id,title,*args,**kwargs):
        self.id = kwargs.get('id',None)
        self.post_text = post_text
        self.tag_id = tag_id
        self.title = title
        self.tag_name = kwargs.get('tag_name',None)
        self.crt_id = kwargs.get('crt_id',None)
        self.crt_time = kwargs.get('crt_time',None)
        self.upd_id = kwargs.get('upd_id',None)
        self.upd_time = kwargs.get('upd_time',None)
        self.group_id = kwargs.get('group_id',None)
        self.group_name = kwargs.get('group_name', None)
        self.post_like = kwargs.get('post_like',None)
        self.comment_counter = kwargs.get('comment_counter',None)
        self.crt_username = kwargs.get('crt_username',None)