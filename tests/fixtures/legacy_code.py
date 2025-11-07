# Legacy code example that needs migration
class UserManager:
    def __init__(self):
        self.users = []
    
    def add_user(self, name, email):
        # Old style, no validation
        self.users.append({'name': name, 'email': email})
    
    def get_user(self, email):
        for user in self.users:
            if user['email'] == email:
                return user
        return None
