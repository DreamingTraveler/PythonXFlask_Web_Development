import models
import validators
from flask import Blueprint, request, abort, render_template
from flask.views import MethodView
from flask_validate import validate


blueprint = Blueprint('goods', __name__)


class GoodsView(MethodView):

    def get(self):
        # good_type = request.args.get('type')
        # keyword = request.args.get('keyword')
        # page = request.args.get('page', 1)
        # count = request.args.get('count', 12)

        query = models.Goods.query

        #query = query.limit(count).offset(count*(page-1))

        goods_list = query.all()
        goods_total = models.Goods.query.count()
        return render_template('goods/goods.html', 
                               goods_list=goods_list,
                               goods_total=goods_total,
                               args=request.args)


blueprint.add_url_rule('/', view_func=GoodsView.as_view(GoodsView.__name__))
