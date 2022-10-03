from botmd_compiler import compile_bot_md
from os import path
from flask_apiexceptions import ApiException

class CouldNotCompileException(ApiException):
    status_code = 500
    detail = 'Could not compile bot -- no compiler found for this file extension.'

compilers = [
    ('md', compile_bot_md)
]

def compile_bot(name):
    for (ext, compiler) in compilers:
        botpath = f'bots/{name}.{ext}'
        if path.exists(botpath):
            return compiler(botpath)
    raise CouldNotCompileException()