from flask import Flask
# 基础功能
from flask_restful import Api, Resource
# 表单验证
from flask_restful import reqparse
# 数据格式化
# from flask_restful import fields, marshal_with


app = Flask(__name__)
api = Api(app)


# 自动表单验证
parser = reqparse.RequestParser()
parser.add_argument('rate', type=int, help='rate必须是一个数字')


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


class TodoSimple(Resource):
    def get(self, what_todo):
        return {'ToDo': what_todo}


class TestParser(Resource):
    def get(self):
        return {'args': parser.parse_args()}


api.add_resource(HelloWorld, '/Hello', '/hello')
api.add_resource(TodoSimple, '/todo/<string:what_todo>', endpoint='todo_ep')
api.add_resource(TestParser, '/parser')


if __name__ == '__main__':
    for item in app.url_map.iter_rules():
        print(" * Map: http://localhost:5000" + str(item))
    # end for
    print()
    app.run(debug=True)
