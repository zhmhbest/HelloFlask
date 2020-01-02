import os
from flask import Flask

app = Flask(__name__)

# 使用Session必须配置如下信息
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(24)


def get_current_time_string():
    import time
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


@app.route("/")
def index():
    return """
    <ul>
        <li><a href='./cookie'>cookie</a></li>
        <li><a href='./session'>session</a></li>
    </ul>
    """


@app.route("/cookie")
def interface_cookie():
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


@app.route("/session")
def interface_session():
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


if __name__ == '__main__':
    app.run()
