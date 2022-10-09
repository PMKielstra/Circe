from flask import render_template

def compile_bot_rive(_path, name):
    """All Rive code is parsed and run on the client.  This is just a shell for the relevant template."""
    return render_template('botrive.js', name=name)