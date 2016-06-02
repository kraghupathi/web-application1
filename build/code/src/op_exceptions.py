
class AttributeRequired(Exception):
    str = None

    def __init__(self, str):
        self.str = str

    def __str__(self):
        return repr(self.str)

class ConstraintError(Exception):
    str = None
    
    def __init__(self, str):
        self.str = str

    def __str__(self):
        return repr(self.str)

class NotAuthorizedError(Exception):
    str = None
    
    def __init__(self, str):
        self.str = str

    def __str__(self):
        return repr(self.str)
