from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = ''


@app.route("/")
def index():
    return "Hello"


if __name__ == '__main__':
    app.run()
