class NoInfoError(Exception):
    def __init__(self):
        super().__init__("The URL get no video info Please check URL input")

class InvaildFileNameError(Exception):
    def __init__(self):
        super().__init__('The following symbol is not allowed in Windows\n \ / | : * ? < > " ')

class InvaildChoiceError(Exception):
    def __init__(self):
        super().__init__('Choice is out of range / not a int')

class PathNotExistError(Exception):
    def __init__(self):
        super().__init__("The path is not exist")
