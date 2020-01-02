from flask import Flask

app = Flask(__name__)

# 打开调试模式
app.config['DEBUG'] = True


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
