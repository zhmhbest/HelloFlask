from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://<帐号>:<密码>@<HOST>:3306/<数据库名称>'
db = SQLAlchemy(app)


@app.route("/")
def index():
    return "Hello"


if __name__ == '__main__':
    app.run()
