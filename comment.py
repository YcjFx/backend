from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# "E:\flask_mp\test.db"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///E:/数据库/test.db'  # 修改为实际的数据库文件路径
db = SQLAlchemy(app)


class CommenttInfo(db.Model):
    __tablename__ = 'commodity_comment'
    id = db.Column(db.Integer, primary_key=True)
    commodity_id = db.Column(db.Integer)
    comment_user_id = db.Column(db.Integer)
    user_comment = db.Column(db.String(50))
    time = db.Column(db.String(50))

with app.app_context():
    #添加评论
    new_data = CommenttInfo(commodity_id = '1000006', comment_user_id = '上善若水', user_comment = '商家人很好，质量也很高，发货很快（一条1毛，括号内删）', time =datetime.now())
    db.session.add(new_data)
    db.session.commit()

    #此处可设置接口，通过接受商品号输出对应信息
    shangpin_id = '1000006'
    search_data = CommenttInfo.query.filter_by(commodity_id = shangpin_id)
    for i in search_data:
        print(i.comment_user_id, i.user_comment, i.time)