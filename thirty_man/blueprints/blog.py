from flask import Blueprint, render_template, request, current_app, flash, url_for, redirect, abort, make_response
from thirty_man.models import Category, Post, Comment
from thirty_man.forms import CommentForm, AdminCommentForm
from thirty_man.extensions import db
from flask_login import current_user
from thirty_man.emails import send_new_reply_email, send_new_comment_email
from thirty_man.utils import redirect_back



blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/change_theme/<theme_name>')
def change_theme(theme_name):
    if theme_name not in current_app.config['BLOG_THEMES'].keys():
        abort(404)

    response = make_response(redirect_back())
    response.set_cookie('theme', theme_name, max_age=30*24*60*60)
    return response




@blog_bp.route('/show_category/<int:category_id>')
def show_category(category_id):
    category = Category.query.get_or_404(category_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['THIRTY_MAN_POST_PER_PAGE']
    pagination = Post.query.with_parent(category).order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)
    posts = pagination.items
    return render_template('blog/show_category.html', category=category, posts=posts, pagination=pagination)


@blog_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)  # 从查询字符串获取当前页数
    per_page = current_app.config['THIRTY_MAN_POST_PER_PAGE']  # 从配置获取每页的数量
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)  # 实例化分页对象
    posts = pagination.items  # 当前页数的记录列表
    return render_template('index.html', posts=posts, pagination=pagination)


@blog_bp.route('/about')
def about():
    return render_template('blog/about.html')


@blog_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['THIRTY_MAN_POST_PER_PAGE']
    comments = Comment.query.with_parent(post).order_by(Comment.timestamp.desc()).all()
    pagination = Comment.query.with_parent(post).order_by(Comment.timestamp.desc()).paginate(page, per_page=per_page)

    if current_user.is_authenticated:
        form = AdminCommentForm()
        form.author.data = current_user.name
        form.email.data = current_app.config['THIRTY_MAN_EMAIL']
        form.site.data = url_for('blog.index')
        from_admin = True
        reviewed = True
    else:
        form = CommentForm()
        from_admin = False
        reviewed = False

    if form.validate_on_submit():
        author = form.author.data
        email = form.email.data
        site = form.site.data
        body = form.body.data
        comment = Comment(
            author=author, email=email, site=site, body=body, from_admin=from_admin, reviewed=reviewed, post=post
        )
        replied_id = request.args.get('reply')
        if replied_id:
            replied_comment = Comment.query.get_or_404(replied_id)
            comment.replied = replied_comment
            send_new_reply_email(replied_comment)
        db.session.add(comment)
        db.session.commit()
        if current_user.is_authenticated:
            flash('评论添加成功')
        else:
            flash('你的评论将在审核后被发布')
            send_new_comment_email(post)
        redirect(url_for('blog/show_post', post_id=post_id))
    return render_template('blog/show_post.html', post=post, form=form, comments=comments, pagination=pagination)


@blog_bp.route('/reply_comment/<int:comment_id>')
def reply_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    return redirect(url_for('blog.show_post', post_id=comment.post_id, reply=comment_id, author=comment.author) + '#comment_form')
