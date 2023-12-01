
class StoreException(Exception):
    def __init__(self, message):
        super().__init__(message)

class StoreExceptionInvalidID(Exception):
    def __init__(self, message):
        super().__init__(message)

class StoreExceptionInvalidDepartmentID(Exception):
    def __init__(self, message):
        super().__init__(message)

class StoreExceptionInvalidProductID(Exception):
    def __init__(self, message):
        super().__init__(message)



