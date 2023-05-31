from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:/001_CODE_PROJECTS/JNU/test.db'   # 修改为实际的数据库文件路径
db = SQLAlchemy(app)

#value_info表
class ValueInfo(db.Model):
    __tablename__ = 'value_info'
    id = db.Column(db.Integer, primary_key=True) #表格索引号
    commodity_id = db.Column(db.Integer) #商品号
    value_user_id = db.Column(db.Integer) #点击值或不值按钮的用户id
    isvalue = db.Column(db.Enum('true','false')) #标记值1或不值0，只能二选一，点击一次不能修改

def Value_add():

    v=[0]*5
    v[0] = ValueInfo(commodity_id=100001, value_user_id=2023001, isvalue='true')
    v[1] = ValueInfo(commodity_id=100001, value_user_id=2023002, isvalue='false')
    v[2] = ValueInfo(commodity_id=100001, value_user_id=2023003, isvalue='true')
    v[3] = ValueInfo(commodity_id=100002, value_user_id=2023001, isvalue='false')
    v[4] = ValueInfo(commodity_id=100002, value_user_id=2023002, isvalue='true')

    for i in range(0,5):
        db.session.add(v[i])
        db.session.commit()
    num_count = ValueInfo.query.filter(ValueInfo.commodity_id==100001).count()
    val_count = ValueInfo.query.filter(ValueInfo.commodity_id==100001, ValueInfo.isvalue=='true').count()
    print("总数：", num_count,"值：", val_count)

with app.app_context():
     db.create_all()
    # db.drop_all()

    # new_com_id = ValueInfo(commodity_id = 1,value_user_id = 1,isvalue = 'true')
    # db.session.add(new_com_id)
    #
    # db.session.commit()
     Value_add()