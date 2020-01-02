from flask import Flask, redirect

app = Flask(
    __name__,
    static_folder="static",          # 静态文件所在目录
    static_url_path="/static_pages"  # 访问静态文件的前缀URL
)


@app.route("/")
def index():
    return redirect("/static_pages/index.html")


if __name__ == '__main__':
    app.run()
