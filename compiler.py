from botmd_compiler import compile_bot_md
from botrive_compiler import compile_bot_rive
from os import path, listdir
from flask_apiexceptions import ApiException
from flask import current_app

class CouldNotCompileException(ApiException):
    status_code = 500
    def __init__(self, message):
        self.message = message
        super().__init__(message)

compilers = [
    ('md', compile_bot_md),
    ('rive', compile_bot_rive)
]

def compile_bot(name):
    botfolder = current_app.config['BOT_FOLDER']
    for (ext, compiler) in compilers:
        botpath = f'{botfolder}/{name}.{ext}'
        if path.exists(botpath):
            return compiler(botpath, name)
    raise CouldNotCompileException(f'No compilable file found for bot {name}.')

def check_bot(ext):
    for (cext, _) in compilers:
        if ext == cext:
            return True
    return False

def list_bots():
    possible_bots = listdir(current_app.config['BOT_FOLDER'])
    split_bots = [path.splitext(b) for b in possible_bots]
    return [name for (name, ext) in split_bots if check_bot(ext[1:])] # Remove the starting period from the extension