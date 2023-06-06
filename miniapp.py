from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import sys
from flask_cors import CORS
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///E:/flask_mp/test.db'
db = SQLAlchemy(app)
#允许跨域请求
CORS(app)

#userinfo表格
class UserInfo(db.Model):
    __tablename__ = 'user_info'
    id = db.Column(db.Integer, primary_key=True)  # 表格索引号
    user_id = db.Column(db.Integer)  # 用户账号
    wx_id = db.Column(db.String(50))  # 微信号
    state = db.Column(db.Integer)  # 账号状态

#commodity_info表格
class CommodityInfo(db.Model):
    __tablename__ = 'commodity_info'
    id = db.Column(db.Integer, primary_key=True)  # 表格索引号
    user_id = db.Column(db.Integer)   #发布用户号
    commodity_id = db.Column(db.Integer)  #商品号
    commodity_name= db.Column(db.String(50))   #商品名
    commodity_desc = db.Column(db.String(50))   #商品描述内容
    commodity_img = db.Column(db.String(50))  #商品图片路径
    commodity_price = db.Column(db.String(50))  #商品价格
    commodity_eshop = db.Column(db.String(50))  #商店名称
    commodity_eurl = db.Column(db.String(50)) #电商链接（可选）
    release_time = db.Column(db.String(50)) #发布时间
    is_verify = db.Column(db.Enum('true','false'))  #是否审核

#value_info表
class ValueInfo(db.Model):
    __tablename__ = 'value_info'
    id = db.Column(db.Integer, primary_key=True)    #表格索引号
    commodity_id = db.Column(db.Integer)  #商品号
    value_user_id = db.Column(db.Integer)  #点击值或不值按钮的用户id
    isvalue = db.Column(db.Integer)  #标记值1或不值0，只能二选一，点击一次不能修改

#collect_info表
class CollectInfo(db.Model):
    __tablename__ = 'commodity_collect'
    id = db.Column(db.Integer, primary_key=True)
    commodity_id = db.Column(db.Integer)
    iscollect=db.Column(db.Enum('true','false'))  #是否点击收藏
    collect_user_id = db.Column(db.Integer)
    collect_time = db.Column(db.String(50))

#comment_info
class CommenttInfo(db.Model):
    __tablename__ = 'commodity_comment'
    id = db.Column(db.Integer, primary_key=True)
    commodity_id = db.Column(db.Integer)
    comment_user_id = db.Column(db.Integer)
    user_comment= db.Column(db.String(50))
    time = db.Column(db.String(50))

#登录页面处理
@app.route('/login', methods=['GET','POST'])
def login():
    postdata=request.get_json()  #字典
    print(postdata, file=sys.stderr)

#主页处理
@app.route('/index', methods=['GET', 'POST'])
def index():
    img = CommodityInfo.commodity_img
    name = CommodityInfo.commodity_name
    price = CommodityInfo.commodity_price
    shop = CommodityInfo.commodity_eshop
    results = CommodityInfo.query.order_by(img, name, price, shop).limit(5).all()
    data = {'data': [
        {'imageSrc': r.commodity_img, 'title': r.commodity_name, 'price': r.commodity_price,
         'eshop': r.commodity_eshop} for r in results]}
    redata = jsonify(data)
    return redata

#商品详情页处理页
@app.route('/shop', methods=['GET', 'POST'])
def shop():
    postdata = request.get_json()  # 字典
    #获取商品图片路径
    imgpath=postdata['commodity_img']
    search_data = CommodityInfo.query.filter_by(commodity_img=imgpath)
    commodity_id=int(imgpath[12:19])
    comment_data = CommenttInfo.query.filter_by(commodity_id=commodity_id)

    # 查询value值
    count = ValueInfo.query.with_entities(func.count(ValueInfo.commodity_id)).filter_by(
        commodity_id=commodity_id).scalar()
    iscount = ValueInfo.query.with_entities(func.count(ValueInfo.commodity_id)).filter_by(
        commodity_id=commodity_id, isvalue='1').scalar()
    nocount = ValueInfo.query.with_entities(func.count(ValueInfo.commodity_id)).filter_by(
        commodity_id=commodity_id, isvalue='0').scalar()
    isratio = round(iscount / count, 4)
    noratio = round(nocount / count, 4)
    ispercentage = "{:.2%}".format(isratio)
    nopercentage = "{:.2%}".format(noratio)

    #查询是否收藏
    iscollect = False
    collectdata=CollectInfo.query.filter_by(commodity_id=commodity_id,collect_user_id =2023001).all()
    if len(collectdata) != 0:
        if (len(collectdata) != 0):
            if(collectdata[0].iscollect=='true'):
                iscollect = True

    data = {'data': [
                    {'comImageSrc': r.commodity_img, 'comPrice': r.commodity_price,
                     'comShop': r.commodity_eshop,'comWriter':r.user_id, 'comName':r.commodity_name,
                     'comDesc': r.commodity_desc }for r in search_data],
            'comments':[i.user_comment for i in comment_data],
            'percentage_data':{'ispercentage': ispercentage,
                               'nopercentage': nopercentage},
            'iscollect':iscollect,
    }
    redata = jsonify(data)
    return redata

#评论区处理
@app.route('/comment', methods=['GET', 'POST'])
def comment():
    postdata = request.get_json()  # 字典
    print(postdata, file=sys.stderr)
    # print(postdata['comImageSrc'][12:19])
    new_data = CommenttInfo( commodity_id=int(postdata['comImageSrc'][12:19]),
                             comment_user_id=postdata['comment_user_id'],
                             user_comment=postdata['newComment'],
                             time=postdata['time'])
    db.session.add(new_data)
    db.session.commit()
    return 'success'

#值或不值处理
@app.route('/value', methods=['GET', 'POST'])
def value():
    postdata = request.get_json()  # 字典
    print(postdata, file=sys.stderr)
    print(postdata['comImageSrc'][12:19],file=sys.stderr)
    new_data = ValueInfo( commodity_id=int(postdata['comImageSrc'][12:19]),
                          value_user_id=postdata['value_user_id'],
                          isvalue=postdata['index'])
    db.session.add(new_data)
    db.session.commit()
    count = ValueInfo.query.with_entities(func.count(ValueInfo.commodity_id)).filter_by(
        commodity_id=int(postdata['comImageSrc'][12:19])).scalar()
    iscount=ValueInfo.query.with_entities(func.count(ValueInfo.commodity_id)).filter_by(
        commodity_id=int(postdata['comImageSrc'][12:19]),isvalue='1').scalar()
    nocount = ValueInfo.query.with_entities(func.count(ValueInfo.commodity_id)).filter_by(
        commodity_id=int(postdata['comImageSrc'][12:19]), isvalue='0').scalar()
    isratio=round(iscount / count, 4)
    noratio=round(nocount / count, 4)
    ispercentage = "{:.2%}".format(isratio)
    nopercentage = "{:.2%}".format(noratio)
    percentage_data = {'ispercentage': ispercentage,
                       'nopercentage': nopercentage}
    redata = jsonify(percentage_data)
    return redata


#发布页面处理
@app.route('/publish', methods=['GET','POST'])
def publish():
    postdata=request.get_json()  #字典
    #图片路径
    imgpath="/images/img/"+str(postdata['com_id'])+'.jpg'

    new_data = CommodityInfo(user_id=postdata['user_id'],
                             commodity_id=postdata['com_id'],
                             commodity_name=postdata['inputName'],
                             commodity_desc=postdata['inputDesc'],
                             commodity_img=imgpath,
                             commodity_price=postdata['inputPrice'],
                             commodity_eshop=postdata['inputShop'],
                             commodity_eurl=postdata['inputUrl'],
                             release_time=postdata['release_time'],
                             is_verify=postdata['is_verify'])
    db.session.add(new_data)
    db.session.commit()
    all_data = CommodityInfo.query.all()
    print(all_data, file=sys.stderr)
    return 'success'



@app.route('/upload', methods=['GET', 'POST'])
def upload():
    # "E:\BaiduNetdiskDownload\3. 手把手教你微信小程序\微信小程序基础\微信小程序基础-资料\day02\代码\mp_02\images\img"
    # "C:\Users\lenovo\Desktop\six\images\img"
    # foldpath="E:/BaiduNetdiskDownload/3. 手把手教你微信小程序/微信小程序基础/微信小程序基础-资料/day02/代码/mp_02/images/img/"
    # foldpath = "/images/img/"
    foldpath ="C:/Users/lenovo/Desktop/six/images/img/"
    file = request.files['file']
    filename = file.filename
    print(filename, file=sys.stderr)
    file.save(foldpath + filename)
    return 'success'


@app.route('/collect', methods=['GET', 'POST'])
def collect():
    postdata = request.get_json()  # 字典
    if(postdata['iscollect']==True):
        new_data = CollectInfo( commodity_id=int(postdata['comImageSrc'][12:19]),
                                collect_user_id=postdata['collect_user_id'],
                                iscollect='true',
                                collect_time=postdata['collect_time'])
        db.session.add(new_data)
        db.session.commit()
    else:
        # 删除 value 属性中数值为 1 的记录
        CollectInfo.query.filter_by(commodity_id=int(postdata['comImageSrc'][12:19]),
                                    collect_user_id=postdata['collect_user_id']).delete()
        db.session.commit()
    return 'success'


@app.route('/work', methods=['GET', 'POST'])
def work():

    results = CommodityInfo.query.filter_by(user_id=2023001).all()
    count = CommodityInfo.query.with_entities(func.count(CommodityInfo.user_id)).filter_by(
                user_id=2023001).scalar()
    data = {'data': [{'imageSrc': r.commodity_img, 'title': r.commodity_name, 'price': r.commodity_price,
                    'eshop': r.commodity_eshop} for r in results],
            'count':count
            }
    print(data, file=sys.stderr)
    redata = jsonify(data)
    return redata


@app.route('/mycollect', methods=['GET', 'POST'])
def mycollect():
    collectdata=CollectInfo.query.filter_by(collect_user_id=2023001).all()
    collects=[co.commodity_id for co in collectdata]
    results = CommodityInfo.query.filter(CommodityInfo.commodity_id.in_(collects)).all()

    data = {'data': [{'imageSrc': r.commodity_img, 'title': r.commodity_name, 'price': r.commodity_price,
                     'eshop': r.commodity_eshop} for r in results]
            }
    print(data, file=sys.stderr)
    redata = jsonify(data)
    return redata



@app.route('/collect_menu', methods=['GET', 'POST'])
def collect_menu():
    postdata = request.get_json()  # 字典
    #删除收藏
    CollectInfo.query.filter_by(commodity_id=int(postdata['comImageSrc'][12:19]),
                                collect_user_id=postdata['collect_user_id']).delete()
    db.session.commit()
    return 'success'


@app.route('/work_menu', methods=['GET', 'POST'])
def work_menu():
    postdata = request.get_json()  # 字典
    print(postdata, file=sys.stderr)

    # 删除商品收藏表相关信息
    CollectInfo.query.filter_by(commodity_id=int(postdata['comImageSrc'][12:19])).delete()
    db.session.commit()

    # 删除商品评论表相关信息
    CommenttInfo.query.filter_by(commodity_id=int(postdata['comImageSrc'][12:19])).delete()
    db.session.commit()

    # 删除商品值或不值表相关信息
    ValueInfo.query.filter_by(commodity_id=int(postdata['comImageSrc'][12:19])).delete()
    db.session.commit()

    # 删除商品信息表相关信息
    CommodityInfo.query.filter_by(commodity_id=int(postdata['comImageSrc'][12:19]),
                                  user_id=postdata['collect_user_id']).delete()
    db.session.commit()
    return 'success'


@app.route('/search', methods=['GET', 'POST'])
def search():
    postdata = request.get_json()  # 字典
    print(postdata, file=sys.stderr)
    search_str=postdata['searchdata']

    results = CommodityInfo.query.filter(CommodityInfo.commodity_name.like(f'%{search_str}%')).all()
    data = {'data': [
        {'imageSrc': r.commodity_img, 'title': r.commodity_name, 'price': r.commodity_price,
         'eshop': r.commodity_eshop} for r in results]}
    redata = jsonify(data)
    return redata

    #搜索查询

    # return 'success'




# 查询表格中所有数据
if __name__ == '__main__':
    app.run()