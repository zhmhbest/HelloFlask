from flask import Flask

app = Flask(
    __name__,
    static_folder="static",          # 静态文件所在目录（默认为static）
    static_url_path="/static_pages"  # 访问静态文件的前缀URL（默认为/static）
)


@app.route("/")
def index():
    from flask import redirect
    return redirect("/static_pages/index.html")


if __name__ == '__main__':
    app.run()
