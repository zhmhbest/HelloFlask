from flask import Flask

"""
    【初始化App】
    以模块__name__所在目录为启动目录
    静态目录：默认为启动目录下的static目录
    模板目录：默认为启动目录下的templates目录
    app = Flask(
        __name__,
        static_folder="static",
        static_url_path="/static",
        template_folder="templates"
    )

"""
app = Flask(__name__)

"""
    【配置文件】
"""

# app.config.from_json("config.json")
# app.config.from_pyfile("config.py")
# app.config.from_object(
#     type("", (), {
#         '__init__': (lambda self, **kwargs: self.__dict__.update(kwargs)),
#         '__eq__': (lambda self, other: self.__dict__ == other.__dict__)
#     })(
#         DEBUG=True,
#     )
# )
app.config['DEBUG'] = True
app.config['KEY_TEST'] = "ABC_"

"""
    【接口】
"""


@app.route("/hello")
def interface_hello():
    return "Hello"


# 读取配置文件
@app.route("/read_config")
def interface_config():
    from flask import current_app
    return str(app.config.get('KEY_TEST')) + str(current_app.config.get('KEY_TEST'))


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


# 获取URL后的额外内容
@app.route("/get_url_hash/<hash_url>")
def interface_hash(hash_url):
    return str(hash_url)


# 获取URL后的额外内容，限制额外内容类型
@app.route("/get_url_hash_int/<int:test_id>")
def interface_hash_int(test_id):
    return str(test_id)


# 自定义限制
def __create_converter__():
    from werkzeug.routing import BaseConverter

    class _RegexConverter(BaseConverter):
        def __init__(self, url_map, regex):
            super(_RegexConverter, self).__init__(url_map)
            self.regex = regex

        def to_python(self, value):
            # to_python方法决定返回值
            return super().to_python(value)

        def to_url(self, value):
            # 决定使用url_for时获取到的值
            return super().to_url(value)

    class _MobileConverter(BaseConverter):
        def __init__(self, url_map):
            super(_MobileConverter, self).__init__(url_map)
            self.regex = r"1[345678]\d{9}"

    class _MailConverter(BaseConverter):
        def __init__(self, url_map):
            super(_MailConverter, self).__init__(url_map)
            self.regex = r"\w+@\w+(\.\w+)+"

    app.url_map.converters['re'] = _RegexConverter
    app.url_map.converters['mobile'] = _MobileConverter
    app.url_map.converters['mail'] = _MailConverter
# end def


__create_converter__()


# 匹配手机号
@app.route(r"/get_url_hash_re/<re(r'1[345678]\d{9}'):pattern>")
def interface_hash_re(pattern):
    return str(pattern)


# 匹配手机号
@app.route(r"/get_url_hash_mobile/<mobile:val_mobile>")
def interface_hash_mobile(val_mobile):
    return str(val_mobile)


# 匹配邮箱
@app.route(r"/get_url_hash_mail/<mail:val_mail>")
def interface_hash_mail(val_mail):
    return str(val_mail)


# error
@app.errorhandler(500)
def on_error_500_message(err):
    return "自定义500错误信息：%s" % err


# abort-error
@app.route("/abort")
def interface_abort():
    from flask import abort
    abort(500)


# response1
@app.route("/response1")
def interface_response1():
    from flask import make_response, Response
    import json
    # response = Response()
    response = make_response(json.dumps({
        'Response': 'Response'
    }))
    response.status = "200"
    response.headers['Content-Type'] = 'text/json'
    return response


# response2
@app.route("/response2")
def interface_response2():
    import json
    return json.dumps({
        'Response': 'Tuple'
    }), 200, {
        'Content-Type': 'text/json'
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
    print(request.headers.items())
    msg = {
        'method': request.method,
        'data': str(request.data, encoding="utf-8"),
        'args': request.args,
        'form': request.form,
        'cookies': request.cookies,
        # 'headers': ,
    }
    return json.dumps(msg), 200, {'Content-Type': 'text/json'}


"""
    【接口】
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
    # app.run()
    app.run(host=HOST, port=PORT)
