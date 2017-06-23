import json
 
class InvalidFilename(Exception):
    pass


class VerificationFile:

    def __init__(self, filename=None):
        self.filename = filename
        if not self.filename:
            raise InvalidFilename('filename cannot be None.')
        self.data = self.read()
    
    def read(self):
        with open(self.filename, 'r') as f:
            data = json.load(f)
        return data
    
    
    def write(self, data=None):
        with open(self.filename, 'w') as f:
            json.dump(data, f)
