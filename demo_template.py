from flask import Flask
from flask import render_template

app = Flask(
    __name__,
    template_folder="templates"  # 模板文件所在目录（默认为templates）
)


@app.route("/")
def index():
    return """
    <ul>
        <li><a href='http://docs.jinkan.org/docs/jinja2/templates.html'>Jinja2帮助文档</a></li>
        <li><a href='./hello'>Hello Template</a></li>
        <li><a href='./filter'>Filter Template</a></li>
    </ul>
    """


@app.route("/hello")
def interface_template_hello():
    data = {
        'title': "Hello Template",
        'test_list': ['a', 'b', 'c'],
        'test_dict': {
            'key1': 'val1',
            'key2': 'val2',
        },
        'a': 1,
        'b': 2,
    }
    return render_template("hello.html", **data)


@app.route("/filter")
def interface_template_filter():
    data = {
        'PI': 3.1415,
        'escape': "<span style='color: red'>Escape String<span>",
        'hello': "hello",
        'HELLO': "HELLO",
        'i_love_you': "i love you",
        'space': "    space    ",
        'test_list': [3, 2, 1, 8, 4, 5],
    }
    return render_template("filter.html", **data)


if __name__ == '__main__':
    app.run()
