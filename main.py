from flask import Flask, Response, render_template, request
from compiler import compile_bot, list_bots

app = Flask(__name__, static_url_path='')

@app.route('/')
def home():
    return render_template('index.html', bots=list_bots())

app.jinja_env.globals.update(compile_bot=compile_bot)
@app.route('/bot/<name>')
def bot(name):
    return render_template('bot.html', name=name, embed=(request.args.get('embed', default='false').lower() == 'true'))

if __name__ == '__main__':
    app.run()