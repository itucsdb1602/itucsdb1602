class Comment:
    #comments are connected its related post that is why __init__ function takes post_id as parameter from posts automatically
    def __init__(self,comment_text,post_id,*args,**kwargs):
        self.id = kwargs.get('id',None)
        self.comment_text = comment_text
        self.post_id = post_id
        self.crt_id = kwargs.get('crt_id',None)
        self.crt_time = kwargs.get('crt_time',None)
        self.upd_id = kwargs.get('upd_id',None)
        self.upd_time = kwargs.get('upd_time',None)
        self.comment_like = kwargs.get('comment_like',None)
        self.crt_username = kwargs.get('crt_username',None)