from flask import Flask, current_app

app = Flask(__name__)

"""
    【从json文件加载配置】
    app.config.from_json("config.json")
"""

"""
    【从py文件加载配置】
    app.config.from_pyfile("config.py")
"""

"""
    【从object中加载配置】
    app.config.from_object(
        type("", (), {
            '__init__': (lambda self, **kwargs: self.__dict__.update(kwargs)),
            '__eq__': (lambda self, other: self.__dict__ == other.__dict__)
        })(
            DEBUG=True,
        )
    )
"""

"""
    直接加载配置
"""
app.config['KEY_TEST'] = "ABC_"


@app.route("/")
def index():
    # 读取配置信息
    return str(app.config.get('KEY_TEST')) + \
           str(current_app.config.get('KEY_TEST'))


if __name__ == '__main__':
    app.run()
