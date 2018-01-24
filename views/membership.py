import models
import validators
from urllib.parse import urlparse, urljoin
from flask import Blueprint,flash, request,  redirect, render_template, session, abort, url_for
from flask.views import MethodView
from flask_validate import validate
from flask_login import login_user, logout_user, current_user, login_required
from flask_bcrypt import Bcrypt

blueprint = Blueprint('membership', __name__)

bcrypt = Bcrypt()

def is_safe_url(target):
        ref_url = urlparse(request.host_url)
        test_url = urlparse(urljoin(request.host_url, target))
        return test_url.scheme in ('http', 'https') and \
            ref_url.netloc == test_url.netloc
            
class LoginView(MethodView):
    def get(self):
        return render_template('membership/login.html')

    @validate(validators.membership.LoginValidator)
    def post(self):
        username = request.form.get('username')
        password = request.form.get('password')

        user = models.Member.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            next = request.args.get('next')
            if not next or not is_safe_url(next):
                return redirect(url_for('membership.ProfileView'))
            return redirect(next)
        return 'XX'

class RegisterView(MethodView):
    def get(self):
        return render_template('membership/register.html')

    @validate(validators.membership.RegisterValidator)
    def post(self):
        username = request.form.get('username')
        password = request.form.get('password')
        realname = request.form.get('realname')
        email = request.form.get('email')
        sex = request.form.get('sex')
        birthday = request.form.get('birthday')
        phone = request.form.get('phone')

        user_exist = models.Member.query.filter_by(username=username).first()
        if user_exist:
            flash('xxx')
            return redirect(url_for('membership.RegisterView'))

        user = models.Member()
        user.username = username
        user.password = bcrypt.generate_password_hash(password)
        user.realname = realname
        user.email = email
        user.sex = sex
        user.birthday = birthday
        user.phone = phone

        models.db.session.add(user)
        models.db.session.commit()
        return 'Registration successful!'

class ProfileView(MethodView):
    @login_required
    def get(self):
        user = current_user
        return render_template('/membership/profile.html', user=user)

    @login_required
    @validate(validators.membership.ProfileValidator)
    def post(self):
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        realname = request.form.get('realname')
        email = request.form.get('email')
        sex = request.form.get('sex')
        birthday = request.form.get('birthday')
        phone = request.form.get('phone')

        user = current_user

        if not bcrypt.check_password_hash(user.password, old_password):
            return 'The old password is wrong!'

        
        user.realname = realname
        user.email = email
        user.sex = sex
        user.birthday = birthday
        user.phone = phone
        if new_password:
            user.password = bcrypt.generate_password_hash(new_password)
        models.db.session.commit()
        return redirect(url_for('membership.ProfileView'))
class LogoutView(MethodView):
    @login_required
    def get(self):
        logout_user()
        return redirect(url_for('index'))

blueprint.add_url_rule('/login', view_func=LoginView.as_view(LoginView.__name__))
blueprint.add_url_rule('/register', view_func=RegisterView.as_view(RegisterView.__name__))
blueprint.add_url_rule('/profile', view_func=ProfileView.as_view(ProfileView. __name__))
blueprint.add_url_rule('/logout', view_func=LogoutView.as_view(LogoutView.__name__))