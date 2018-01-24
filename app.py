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

    goods = models.Goods()
    goods.name = 'GJDLJGLA'
    goods.state = 'To sell'
    goods.type = goods_type
    goods.author = member
    goods.description = '''ka[dsg ks[dkfm[aosdkr]papsk f]pok kapflklkalks [pk[
        dgkds sd;lf';l d;s
        [ a[lsdf'
         sd; klsdk; lfkps;dlpfl, sp;l
         sdf ;lkl;sdk ;lksd;lkf[pqle[prk '''
    goods.image = '/static/images/cat4.jpg'

    models.db.session.add(goods)
    models.db.session.commit()



@app.route('/')
def index():
    return render_template('base/index.html')

if __name__ == '__main__':
    cli()