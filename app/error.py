class UserNotLogin(Exception):
    def __init__(self):
        super().__init__()


class PrivateProject(Exception):
    def __init__(self):
        super().__init__()


class FileIsEmpty(Exception):
    def __init__(self):
        super().__init__()


class FileIsTooBig(Exception):
    def __init__(self):
        super().__init__()
