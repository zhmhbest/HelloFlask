from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return """
    <ul>
        <li><a href='./get_url_hash/ABCD1234'>获取URL后的额外内容</a></li>
        <li><a href='./get_url_hash_int/1234'>获取URL后的额外内容（限制为数字）</a></li>
        <li><a href='./get_url_hash_re/18887643217'>RE匹配手机号</a></li>
        <li><a href='./get_url_hash_mobile/18887643217'>匹配手机号</a></li>
        <li><a href='./get_url_hash_mail/123@456.com'>匹配邮箱</a></li>
    </ul>
    """


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


if __name__ == '__main__':
    app.run()
