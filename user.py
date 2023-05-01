from werkzeug.security import check_password_hash

class User:
    def __init__(self, id, email, password,balance,name):
        self.id = id
        self.name=name
        self.email = email
        self.password_hash = password
        self.balance = balance

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_active(self):
        return True

    def get_id(self):
        return str(self.id)

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False
