import os
from flask import Flask, render_template, redirect, request, flash, url_for, get_flashed_messages
from thirty_man.blueprints.auth import auth_bp
from thirty_man.blueprints.admin import admin_bp
from thirty_man.blueprints.blog import blog_bp
from thirty_man.extensions import db, mail, bootstrap, moment, loginmanager, csrf, ckedtor, migrate, sslify
from thirty_man.commands import register_commands
from thirty_man.models import Admin, Category, Post, Link, Comment
from thirty_man.setting import config
from flask_login import current_user



def create_app(config_name=None):
    # 创建实例
    app = Flask(__name__)
    # 判断配置参数
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    # 配置
    app.config.from_object(config[config_name])
    # 注册蓝本、扩展、命令行
    register_blueprint(app)
    register_extensions(app)
    register_commands(app)
    register_template_context(app)

    return app


def register_blueprint(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(blog_bp, url_prefix='/blog')


def register_extensions(app):
    db.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    loginmanager.init_app(app)
    csrf.init_app(app)
    ckedtor.init_app(app)
    migrate.init_app(app, db)
    sslify.init_app(app)


def register_template_context(app):
    @app.context_processor
    def make_template_context():
        admin = Admin.query.first()
        categories = Category.query.order_by(Category.name).all()
        links = Link.query.order_by(Link.name).all()
        if current_user.is_authenticated:
            unread_comments = Comment.query.filter_by(reviewed=False).count()
        else:
            unread_comments = None
        return dict(
            admin=admin, categories=categories,
            links=links, unread_comments=unread_comments)