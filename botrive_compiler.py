from flask import render_template

def compile_bot_rive(_path, name):
    return render_template('botrive.js', name=name)