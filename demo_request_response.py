from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return """
    <ul>
        <li><a href='./response1'>response1</a></li>
        <li><a href='./response2'>response2</a></li>
        <li><a href='./request'>request</a></li>
    </ul>
    """


@app.route("/response1")
def interface_response1():
    return "<h1>Response: directly return</h1>", 200, {
        'Content-Type': 'text/html'
    }


@app.route("/response2")
def interface_response2():
    from flask import make_response
    response = make_response("<h1>Response: make response</h1>")
    response.status = "200"
    response.headers['Content-Type'] = 'text/html'
    return response


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


if __name__ == '__main__':
    app.run()
