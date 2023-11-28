
class StoreException(Exception):
    def __init__(self, message):
        super().__init__(message)

class StoreExceptionInvalidID(Exception):
    def __init__(self, message):
        super().__init__(message)
