from flask import Flask, Response, render_template, request
from compiler import CouldNotCompileException, compile_bot, list_bots

app = Flask(__name__, static_url_path='')

@app.route('/')
def home():
    return render_template('index.html', bots=list_bots())

app.jinja_env.globals.update(compile_bot=compile_bot)
@app.route('/bot/<name>')
def bot(name):
    try:
        return render_template('bot.html', name=name, embed=(request.args.get('embed', default='false').lower() == 'true'))
    except CouldNotCompileException as e:
        return render_template('bot_err.html', exception=e.message)

if __name__ == '__main__':
    app.run()