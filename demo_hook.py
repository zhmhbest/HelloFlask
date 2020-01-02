from flask import Flask
from flask import request

app = Flask(__name__)


@app.route("/")
def index():
    print("Index")
    return "Hello Hook"


@app.before_first_request
def handle_before_first_request():
    print("第一次请求之前")


@app.before_request
def handle_before_request():
    print("请求之前")


@app.after_request
def handle_after_request(response):
    print("请求之后（视图函数无异常）", request.path)
    return response


@app.teardown_request
def handle_teardown_request(response):
    print("请求之后（总是会在请求完成后执行）", request.path)
    return response


if __name__ == '__main__':
    app.run()
