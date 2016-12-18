class PostKeywords:
    def __init__(self,keywords_id,post_id, *args, **kwargs ):
        self.keywords_id = keywords_id
        self.post_id = post_id
        self.keywords_name = kwargs.get('keywords_name',None)

