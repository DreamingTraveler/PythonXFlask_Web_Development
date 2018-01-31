import config
import click
import views
import models
from flask import Flask, request, render_template, Blueprint
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask.cli import FlaskGroup

app = Flask(__name__, static_url_path='/static')
app.config.from_object(config)
models.db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'
login_manager.login_message = 'Bonvolu ensaluti por uzi tiun paĝon.'

@login_manager.user_loader
def load_user(user_id):
    return models.Member.query.filter_by(id=user_id).first()

app.register_blueprint(views.membership.blueprint, url_prefix='/membership')
app.register_blueprint(views.goods.blueprint, url_prefix='/goods')

def create_app(info=None):
    return app

cli = FlaskGroup(create_app=create_app)

@cli.command()
def initdb():
    click.echo('Init the db')
    models.db.drop_all()
    models.db.create_all()

@cli.command()
def create_testdata():
    click.echo('Create test data.')

    member = models.Member()
    member.username = 'qqq123'
    member.password = views.membership.bcrypt.generate_password_hash('123123')
    member.realname = 'Liszt'
    member.email = 'liszt@gmail.com'
    member.sex = 'male'
    member.phone = '0356225446'
    member.permission = 0x1
    models.db.session.add(member)

    goods_type = models.GoodsType()
    goods_type.size = 'L'
    goods_type.state = 'test'
    goods_type.price = 682
    models.db.session.add(goods_type)

    goods_type_m = models.GoodsType()
    goods_type_m.size = 'M'
    goods_type_m.state = 'test'
    goods_type_m.price = 881
    models.db.session.add(goods_type_m)

    for i in range(1,730):
        goods = models.Goods()
        goods_image1 = models.GoodsImages()
        goods_image1.goods = goods
        goods.state = 'To sell'
        if i % 2 == 0:
            goods_image2 = models.GoodsImages()
            goods_image2.goods = goods
            goods.name = 'KITTEN 曉貓'+ str(i)
            goods.type = goods_type
            goods_image1.image = '/static/images/cat4.jpg'
            models.db.session.add(goods_image1)
            goods_image2.image = '/static/images/cat2.jpg'
            models.db.session.add(goods_image2)
        else:
            goods.name = 'BIRD_AND_CAT 鳥&貓 '+ str(i)
            goods.type = goods_type_m
            goods_image1.image = '/static/images/cat3.jpg'
            models.db.session.add(goods_image1)
        goods.author = member
        goods.description = '''ka[dsg ks[dkfm[aosdkr]papsk f]pok kapflklkalks [pk[
            dgkds sd;lf';l d;s
            [ a[lsdf'
            sd; klsdk; lfkps;dlpfl, sp;l
            sdf ;lkl;sdk ;lksd;lkf[pqle[prk '''
        models.db.session.add(goods)

    order = models.Order()
    order.amount = 881
    order.purchaser = member
    models.db.session.add(order)

    order_item = models.OrderItem()
    order_item.quantity = 1
    order_item.goods = goods
    order_item.order = order
    models.db.session.add(order_item)

    comment1 = models.Comment()
    comment1.author = member
    comment1.goods = goods
    comment1.message = '?????????渣SA{DQ@ㄉ@``CSCf;ll;z;'
    models.db.session.add(comment1)

    comment2 = models.Comment()
    comment2.author = member
    comment2.goods = goods
    comment2.message = '爛!!!!!!!!!afgbbxvxv豬ad45675O--i092I0U302909JPJR3'
    models.db.session.add(comment2)

    comment3 = models.Comment()
    comment3.author = member
    comment3.goods = goods
    comment3.message = 'xafaxoooooofafos@肥豬鷹!XXXXXXXXXXXXXXXXXXXXX'
    models.db.session.add(comment3)

    rating2 = models.Rating()
    rating2.author = member
    rating2.for_order_item = order_item
    rating2.score = 1
    rating2.message = '爛!!!!!!!!!afasjfjKJEPKRJPO--i092I0U302909JPJR3'
    models.db.session.add(rating2)

    rating = models.Rating()
    rating.author = member
    rating.for_order_item = order_item
    rating.score = 3
    rating.message = 'sdogkpa!I@(_)_)UafF())I#){(RU)USJOJIJLKJlj ojroqi *&:((((('
    models.db.session.add(rating)

    rating2 = models.Rating()
    rating2.author = member
    rating2.for_order_item = order_item
    rating2.score = 1
    rating2.message = '爛!!!!!!!!!afasjfjKJEPKRJPO--i092I0U302909JPJR3'
    models.db.session.add(rating2)

    models.db.session.commit()
@app.route('/')
def index():
    return render_template('base/index.html')

if __name__ == '__main__':
    cli()