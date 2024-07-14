class Session:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Session, cls).__new__(cls)
            cls._instance.user_data = None
        return cls._instance

    def set_user_data(self, data):
        self.user_data = data

    def get_user_data(self):
        return self.user_data
