from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, username, email, passwordHash, fullname, gender):
        self.id = None
        self.username = username
        self.email = email
        self.passwordHash = passwordHash
        self.fullname = fullname
        self.gender = gender

    @property
    def is_authenticated(self):
        if self.id:
            return True
        return False

    def get_id(self):
        return str(self.id).encode("utf-8").decode("utf-8")


    def set_id(self, id):
        self.id = id