from botmd_compiler import compile_bot_md
from botrive_compiler import compile_bot_rive
from os import path, listdir
from flask_apiexceptions import ApiException

class CouldNotCompileException(ApiException):
    status_code = 500
    def __init__(self, message):
        self.message = message
        super().__init__(message)

compilers = [
    ('md', compile_bot_md)
#    ('rive', compile_bot_rive)
]

def compile_bot(name):
    for (ext, compiler) in compilers:
        botpath = f'bots/{name}.{ext}'
        if path.exists(botpath):
            return compiler(botpath)
    raise CouldNotCompileException(f'No compilable file found for bot {name}.')

def check_bot(ext):
    for (cext, _) in compilers:
        if ext == cext:
            return True
    return False

def list_bots():
    possible_bots = listdir('bots')
    split_bots = [path.splitext(b) for b in possible_bots]
    return [name for (name, ext) in split_bots if check_bot(ext[1:])] # Remove the starting period from the extension