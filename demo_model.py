from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

"""
    配置
"""


class Config:
    DEBUG = True
    SQL_CONFIG = {
        'host': '39.107.96.222',
        'port': '3306',
        'user': 'wzd',
        'password': '!@#$%RDX123ad',
        'database': 'flask',
    }
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://<帐号>:<密码>@<HOST>:3306/<数据库名称>'
    SQLALCHEMY_DATABASE_URI = 'mysql://' + \
                              SQL_CONFIG['user'] + ':' + \
                              SQL_CONFIG['password'] + '@' + \
                              SQL_CONFIG['host'] + ':' + \
                              SQL_CONFIG['port'] + '/' + \
                              SQL_CONFIG['database']

    # 数据被修改时，修改模型类
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 打印SQL语句
    SQLALCHEMY_ECHO = True


app.config.from_object(Config)


"""
    数据库模型
"""
db = SQLAlchemy(app)


class Role(db.Model):
    """
        用户角色/身份表
    """
    __tablename__ = 'tbl_roles'
    id = db.Column(db.BIGINT, primary_key=True, nullable=False, autoincrement=True)
    # 身份名称（不可重复）
    name = db.Column(db.String(32), unique=True)
    # 反向映射外键
    users = db.relationship('User', backref='role')


class User(db.Model):
    """
        用户表
    """
    __tablename__ = 'tbl_users'
    id = db.Column(db.BIGINT, primary_key=True)
    name = db.Column(db.String(32))
    age = db.Column(db.Integer)
    gender = db.Column(db.Boolean)
    account = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(128))
    # 映射外键
    role_id = db.Column(db.BIGINT, db.ForeignKey('tbl_roles.id'))


"""
    接口
"""


def return_html_table(aoa_table, thead=None, title=''):
    """
    返回可视化列表
    :param aoa_table: 在网页中展示的表格
    :param thead: 表格标题（可选）
    :param title: 标题（可选）
    :return:
    """
    buffer = []
    buffer.append("""<style>
        h2 {
            text-align: center;
        }
        table {
            margin-left: 10%;
            margin-right: 10%;
            width:80%;
            border-collapse: collapse;
        }
        /* 标题样式 */
        table>thead {
            font-size: larger;
            background: #999999;
        }
        /* 边框样式 */
        table, td, th {
            border: 1px solid #d4d4d4;
            padding: 5px;
        }
        /* 条纹颜色 */
        tbody tr:nth-child(odd) {
             background: #FFFFFF;
        }
        tbody tr:nth-child(even) {
             background: #F8F8F8;
        }
        /* 悬停效果 */
        tbody tr:hover {
             background: linear-gradient(#fff,#aaa);
        }
    </style>""")
    buffer.append('<h2>')
    buffer.append(title)
    buffer.append('</h2>')
    buffer.append('<table>')
    # Head
    if thead is not None:
        buffer.append('<thead><tr>')
        for item in thead:
            buffer.append('<th>')
            buffer.append(str(item))
            buffer.append('</th>')
        buffer.append('</tr></thead>')
    # Body
    buffer.append('<tbody>')
    for line in aoa_table:
        buffer.append('<tr>')
        for item in  line:
            buffer.append('<th>')
            buffer.append(str(item))
            buffer.append('</th>')
        buffer.append('</tr>')
    buffer.append('</tbody>')
    buffer.append('</table>')
    return ''.join(buffer), 200, {'Content-Type': 'text/html; Charset=utf-8'}


@app.route("/")
def index():
    return """
    <ul>
        <li><a href='./read_all_role'>读取全部Role</a></li>
        <li><a href='./read_all_user'>读取全部User</a></li>
        
        <li><a href='./read_first_role'>读取Role中，第一条数据</a></li>
        <li><a href='./read_by_id'>读取Role中，ID为1的数据</a></li>
        
        <li><a href='./filter_by_from_user'>读取User中，按筛选规则筛选的数据</a></li>
        <li><a href='./filter_from_user'>读取User中，按筛选规则筛选的数据</a></li>
    </ul>
    """


@app.route("/read_all_role")
def read_all_role():
    dat_all = Role.query.all()
    buffer = []
    for item in dat_all:
        buffer.append([item.id, item.name])
    return return_html_table(buffer, ['id', 'name'], '读取全部Role')


@app.route("/read_all_user")
def read_all_user():
    dat_all = User.query.all()
    buffer = []
    for item in dat_all:
        buffer.append([item.id, item.name, item.age, item.gender, item.account, item.password])
    return return_html_table(buffer,
                             ['id', 'name', 'age', 'gender', 'account', 'password'],
                             '读取全部User')


@app.route("/read_first_role")
def read_first_role():
    item = Role.query.first()
    return return_html_table([[item.id, item.name]], ['id', 'name'], '读取第一条Role')


@app.route("/read_by_id")
def read_by_id():
    item = Role.query.get(1)
    return return_html_table([[item.id, item.name]], ['id', 'name'], '读取Role中ID为1的数据')


@app.route("/filter_by_from_user")
def filter_by_from_user():
    dat_all = User.query.filter_by(gender=0, age=18)
    buffer = []
    for item in dat_all:
        buffer.append([item.id, item.name, item.age, item.gender, item.account, item.password])
    return return_html_table(buffer,
                             ['id', 'name', 'age', 'gender', 'account', 'password'],
                             '读取User表中age=18, gender=0, 的数据')


"""
    运行
"""


def db_while_first_run():
    """
    本方法用于初始化数据库
    :return:
    """
    # 根据模型创建数据库表
    db.create_all()

    # 增加数据库数据（创建角色）
    db.session.add(Role(name='本科生'))
    db.session.add(Role(name='研究生'))
    db.session.add(Role(name='博士生'))
    db.session.add(Role(name='宿管'))
    db.session.add(Role(name='讲师'))
    db.session.add(Role(name='副教授'))
    db.session.add(Role(name='教授'))
    db.session.commit()

    # 增加数据库数据（增加用户）
    db.session.add_all([
        User(name='张三', age=18, gender=0, account='zhang3', password='123456'),
        User(name='李四', age=20, gender=1, account='li4', password='123456'),
        User(name='王五', age=18, gender=1, account='wang5', password='159357'),
        User(name='赵六', age=21, gender=1, account='zhao6', password='159357'),
    ])
    db.session.commit()

    # 清楚数据库所有内容
    # db.drop_all()


if __name__ == '__main__':
    from sqlalchemy.exc import ProgrammingError
    try:
        result = Role.query.all()
        print(len(result))
    except ProgrammingError:
        print("读取数据库异常")
        print("尝试创建数据库")
        db_while_first_run()
    # end try
    app.run()
