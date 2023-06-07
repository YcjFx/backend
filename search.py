from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import sys

# "E:\flask_mp\test.db"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///E:/数据库/test.db'  # 修改为实际的数据库文件路径
db = SQLAlchemy(app)

class CommodityInfo(db.Model):
    __tablename__ = 'commodity_info'
    id = db.Column(db.Integer, primary_key=True) # 表格索引号
    user_id = db.Column(db.Integer) #发布用户号
    commodity_id = db.Column(db.Integer) #商品号
    commodity_name= db.Column(db.String(50)) #商品名
    commodity_desc = db.Column(db.String(50)) #商品描述内容
    commodity_img = db.Column(db.String(50)) #商品图片路径
    commodity_price = db.Column(db.String(50)) #商品价格
    commodity_eshop = db.Column(db.String(50)) #商店名称
    commodity_eurl = db.Column(db.String(50)) #电商链接（可选）
    release_time = db.Column(db.String(50)) #发布时间
    is_verify = db.Column(db.Enum('true','false')) #是否审核


with app.app_context():
    #此处可设置接口，通过接受商品号输出对应信息
    shangpin_id = '10001'
    search_data = CommodityInfo.query.filter_by(commodity_id = shangpin_id)
    for i in search_data:
        print(i.commodity_name, i.commodity_img, i.commodity_price, i.commodity_eshop)
