import os
from flask import Flask

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(24)


"""
    【接口】
"""


@app.route("/hello")
def interface_hello():
    return "Hello"


# 同一个URL地址，根据请求方式决定方法
@app.route("/do_by_method_type", methods=['POST'])
def interface_post():
    return "post_only"


# 两个URL地址指向一个方法
@app.route("/do_by_method_type", methods=['GET'])
@app.route("/get_only", methods=['GET'])
def interface_get():
    return "get_only"


# 通过方法名获得其对应的URL地址
@app.route("/get_url_name")
def interface_de_method():
    from flask import url_for
    return url_for("interface_hello")


# 重定向接口
@app.route("/redirect")
def interface_redirect():
    from flask import redirect
    return redirect("/hello")


# response1
@app.route("/response1")
def interface_response1():
    from flask import make_response, Response
    # response = Response()
    response = make_response("<h1>Response1</h1>")
    response.status = "200"
    response.headers['Content-Type'] = 'text/html'
    return response


# response2
@app.route("/response2")
def interface_response2():
    return "<h1>Response2</h1>", 200, {
        'Content-Type': 'text/html'
    }


# request
@app.route("/request")
def interface_request():
    import json
    from flask import request
    # str                                                   request.url
    # str                                                   request.method
    # bytes                                                 request.data
    # werkzeug.datastructures.ImmutableMultiDict            request.form
    # werkzeug.datastructures.ImmutableMultiDict            request.args
    # werkzeug.datastructures.ImmutableTypeConversionDict   request.cookies
    # werkzeug.datastructures.EnvironHeaders                request.headers
    # werkzeug.datastructures.attach_enctype_error_multidict.<locals>.newcls    request.files
    msg = {
        'method': request.method,
        'data': str(request.data, encoding="utf-8"),
        'args': request.args,
        'form': request.form,
        'cookies': request.cookies,
        'headers': dict(request.headers),
    }
    return json.dumps(msg), 200, {'Content-Type': 'text/json'}


# cookie
@app.route("/cookie")
def interface_cookie():
    def get_current_time_string():
        import time
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    # end def

    def get_current_cookies_string():
        import json
        from flask import request
        return json.dumps(request.cookies)
    # end def

    from flask import make_response
    response = make_response(get_current_cookies_string())
    response.headers['Content-Type'] = 'text/json'
    #
    response.set_cookie('cookie_last', get_current_time_string())
    return response


# session
@app.route("/session")
def interface_session():
    def get_current_time_string():
        import time
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    # end def

    def get_current_sessions_string(sess):
        import json
        return json.dumps(dict(sess))
    # end def

    from flask import session
    from flask import make_response
    response = make_response(get_current_sessions_string(session))
    response.headers['Content-Type'] = 'text/json'
    #
    session['session_last'] = get_current_time_string()
    return response


"""
    【启动】
"""
if __name__ == '__main__':
    HOST = "127.0.0.1"
    PORT = 5000
    DOMAIN = "http://" + HOST + ":" + str(PORT)

    # 路由信息
    # print(app.url_map)
    for item in app.url_map.iter_rules():
        print(" *", DOMAIN + str(item))
    # end for
    print()

    # 启动应用
    app.run(host=HOST, port=PORT)
