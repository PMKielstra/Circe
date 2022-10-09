from flask import render_template

def compile_bot_rive(path):
    with open(path, 'r') as file:
        rive_code = file.read().replace('\n', '\\n');
        return render_template('botrive.js', rive_code=rive_code)