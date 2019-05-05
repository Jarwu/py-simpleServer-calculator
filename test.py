from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:88888888@localhost:3306/calculator?charset=utf8'
db = SQLAlchemy(app)


# 映射数据库
class History(db.Model):
    # 表名
    __tablename__ = 'history'
    id = db.Column(db.Integer, primary_key=True, index=True)
    his = db.Column(db.String(120))
    res = db.Column(db.String(120))


@app.route('/')
def index():
    return 'Index Page'


@app.route('/history/list', methods=["GET"])
def history_list():
    res = History.query.all()
    list = []
    # 解构数据库的数据
    for e in res:
        list.append({
            'id': e.id,
            'his': e.his,
            'res': e.res,
        })
    response = {
        'code': 200,
        'res': list,
    }
    # 格式化为json
    return json.dumps(response)


@app.route('/history/add', methods=["POST"])
def history_add():
    data = json.loads(request.data)
    temp1 = data['his']
    temp2 = data['res']
    db.session.add(History(his=temp1, res=temp2))
    db.session.commit()
    response = {
        'code': 200,
        'msg': '添加成功',
        'data': {}
    }
    return json.dumps(response)


@app.route('/history/get', methods=["POST"])
def history_get():
    id = json.loads(request.data)

    result = History.query.filter(History.id == id).first()

    response = {
        'code': 200,
        'msg': '查询成功',
        'data': {
            'id': result.id,
            'his': result.his,
            'res': result.res,
        }
    }

    return json.dumps(response)


@app.route('/history/delete', methods=["DELETE"])
def history_delete():
    id = json.loads(request.data)

    result = History.query.filter(History.id == id).first()
    db.session.delete(result)
    db.session.commit()

    response = {
        'code': 200,
        'msg': '删除成功',
        'data': {}
    }

    return json.dumps(response)


# 主函数
if __name__ == '__main__':
    # 解决跨域请求
    # 知识:https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Access_control_CORS
    # 简单解决:https://blog.csdn.net/yannanxiu/article/details/53036508
    CORS(app, supports_credentials=True)
    # 热更新
    app.debug = True
    app.run()
