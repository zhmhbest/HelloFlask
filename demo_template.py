from flask import Flask
from flask import render_template

app = Flask(
    __name__,
    template_folder="templates"  # 模板文件所在目录（默认为templates）
)


@app.route("/")
def index():
    data = {
        'title': "Hello Template",
        'test_list': ['a', 'b', 'c'],
        'test_dict': {
            'key1': 'val1',
            'key2': 'val2',
        }
    }
    return render_template("template1.html", **data)


if __name__ == '__main__':
    app.run()
