from flask import Flask
from flask import abort

app = Flask(__name__)


# error
@app.errorhandler(500)
def on_error_500_message(err):
    return """
        <h1>自定义500错误信息</h1>
        <p>%s</p>
    """ % err


@app.route("/")
def index():
    abort(500)


if __name__ == '__main__':
    app.run()
