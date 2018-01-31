import models
import validators
import sys
import os
import config
from flask import Blueprint, request, abort, render_template, redirect, url_for, current_app
from flask.views import MethodView
from flask_login import current_user, login_required
from flask_validate import validate
from werkzeug.utils import secure_filename


blueprint = Blueprint('goods', __name__)


class GoodsView(MethodView):

    def get(self):
        good_type = request.args.get('type')
        keyword = request.args.get('search')
        page = request.args.get('page', 1)
        item_count = request.args.get('count', 15)
        query = models.Goods.query

        if good_type:
            query = query.join(models.GoodsType).filter_by(size=good_type)

        if keyword:
            query = query.filter(models.Goods.name.like('%{}%'.format(keyword)))

        query = query.limit(item_count).offset((int(page)-1) * item_count)

        goods_list = query.all()
        goods_total = models.Goods.query.count()
        return render_template('goods/goods.html', 
                               goods_list=goods_list,
                               goods_total=goods_total,
                               args=request.args)
class GoodsDetailView(MethodView):
    def get(self, goods_id):
        goods = models.Goods.query.filter_by(id=goods_id).first()
        image_num = models.GoodsImages.query.filter_by(goods_id=goods_id).count()
        goods_comments = models.Comment.query.filter_by(goods_id=goods_id).all()

        return render_template('goods/detail.html', goods=goods, comments=goods_comments, image_num=image_num)

    @login_required
    def post(self, goods_id):
        message = request.form.get('comment')
        goods = models.Goods.query.filter_by(id=goods_id).first()
        goods_comments = models.Comment.query.filter_by(goods_id=goods_id).all()

        comment = models.Comment()
        comment.author = current_user
        comment.goods = goods
        comment.message = message
        models.db.session.add(comment)
        models.db.session.commit()

        return redirect(url_for('goods.GoodsDetailView', goods_id=goods.id))

class PublishGoodsView(MethodView):
    def get(self):
        return render_template('goods/publish.html')

    @login_required
    def post(self):
        goods_name = request.form.get('goods-name')
        goods_size = request.form.get('size')
        description = request.form.get('description')
        images = request.files.get('images')

        print(request.files.get('images'))
        for image in images:
            print("fasf")
            filename = secure_filename(image.filename)
            image.save(os.path.join(config.UPLOADED_FILES_DEST, filename))
            
        return 'x'


blueprint.add_url_rule('/', view_func=GoodsView.as_view(GoodsView.__name__))
blueprint.add_url_rule('/<int:goods_id>', view_func=GoodsDetailView.as_view(GoodsDetailView.__name__))
blueprint.add_url_rule('/publish_goods', view_func=PublishGoodsView.as_view(PublishGoodsView.__name__))
