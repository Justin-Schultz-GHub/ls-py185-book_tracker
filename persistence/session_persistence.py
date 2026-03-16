class SessionPersistence:
    def __init__(self, session):
        self.session = session

    def login(self, user_id):
        self.session['user_id'] = user_id

    def logout(self):
        self.session.pop('user_id', None)