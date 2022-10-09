from flask import Flask, render_template, request, send_from_directory
from compiler import CouldNotCompileException, compile_bot, list_bots

app = Flask(__name__, static_url_path='')
app.config.from_pyfile('config.py')
app.config.from_prefixed_env('CIRCE')

@app.route('/')
def home():
    return render_template('index.html', bots=list_bots(), motd=app.config['MOTD'])

app.jinja_env.globals.update(compile_bot=compile_bot)
@app.route('/bot/<name>')
def bot(name):
    try:
        return render_template('bot.html', name=name, embed=(request.args.get('embed', default='false').lower() == 'true'))
    except CouldNotCompileException as e:
        return render_template('bot_err.html', exception=e.message)

@app.route('/botstatic/<path>')
def botstatic(path):
    return send_from_directory('bots', path)

app.config['TRAP_HTTP_EXCEPTIONS'] = True
@app.errorhandler(Exception)
def error(e):
    assert(hasattr(e, "code"))
    assert(hasattr(e, "description"))
    return render_template('generic_err.html', exception=e.description), e.code

if __name__ == '__main__':
    app.run()