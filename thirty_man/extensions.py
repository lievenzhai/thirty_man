from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_ckeditor import CKEditor
from flask_migrate import Migrate
from flask_sslify import SSLify


db = SQLAlchemy()
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()
loginmanager = LoginManager()
csrf = CSRFProtect()
ckedtor = CKEditor()
migrate = Migrate()
sslify = SSLify()



@loginmanager.user_loader
def load_user(user_id):
    from thirty_man.models import Admin
    user = Admin.query.get(int(user_id))
    return user


loginmanager.login_view = 'auth.login'
loginmanager.login_message_category = 'warning'
loginmanager.login_message = u'请先登录！'