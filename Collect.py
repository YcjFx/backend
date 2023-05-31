from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:/001_CODE_PROJECTS/JNU/test.db'   # 修改为实际的数据库文件路径
db = SQLAlchemy(app)


# collect_info表
class CollectInfo(db.Model):
    __tablename__ = 'commodity_collect'
    id = db.Column(db.Integer, primary_key=True)
    commodity_id = db.Column(db.Integer)
    iscollect=db.Column(db.Enum('true', 'false')) #是否点击收藏
    collect_uesr_id = db.Column(db.Integer)
    collect_time = db.Column(db.Integer)



# 用户收藏
def collect_add():
    count=CollectInfo.query.filter(CollectInfo.commodity_id==100001,CollectInfo.iscollect=='true').count()#收藏次数统计
    # 用户收藏数据
    c=[0]*4
    c[0] = CollectInfo(commodity_id=100001, iscollect='true', collect_uesr_id=2023002)
    c[1] = CollectInfo(commodity_id=100001, iscollect='true', collect_uesr_id=2023003)
    c[2] = CollectInfo(commodity_id=100002, iscollect='true', collect_uesr_id=2023004)
    c[3] = CollectInfo(commodity_id=100001, iscollect='false', collect_uesr_id=2023002)
    # 判断是否取消收藏
    for i in range(0,4):
        if(c[i].iscollect=='true'):
            count+=1
            db.session.add(c[i])
            db.session.commit()
        else:
            count-=1
            c=CollectInfo.query.filter_by(commodity_id=c[i].commodity_id, collect_uesr_id=c[i].collect_uesr_id).first()
            db.session.delete(c)
            db.session.commit()
    CollectInfo.query.filter(CollectInfo.commodity_id==100001, CollectInfo.iscollect=='true').update({"collect_time":count})#更新收藏次数
    db.session.commit()

# 测试
with app.app_context():
     db.create_all()
    # db.drop_all()

    # new_com_id = ValueInfo(commodity_id = 1,value_user_id = 1,isvalue = 'true')
    # db.session.add(new_com_id)
    #
    # db.session.commit()

     collect_add()