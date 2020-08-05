from thirty_man.extensions import db
from thirty_man.models import Admin, Comment, Category, Post
from faker import Faker
from sqlalchemy.exc import IntegrityError
import random


fake = Faker()


def fake_admin():
    admin = Admin(
        username='管理员',
        blog_title='男人三十',
        blog_sub_title='有趣的灵魂万里挑一',
        name='翟立元',
        about='自从做了父亲，总是想留下点什么'
    )
    admin.set_password('zhailiyuan110')
    db.session.add(admin)
    db.session.commit()


def fake_categories(count=10):
    category = Category(name='默认')
    db.session.add(category)

    for i in range(count):
        category = Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_posts(count=50):
    for i in range(50):
        post = Post(
            title=fake.sentence(),
            body=fake.text(2000),
            category=Category.query.get(random.randint(1, Category.query.count())),
            timestamp=fake.date_time_this_year()
        )
        db.session.add(post)
    db.session.commit()


def fake_comment(count=500):
    for i in range(count):
        comment= Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
    salt = int(count * 0.1)
    # 未被审核的评论
    for i in range(salt):
        comment= Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=False,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
         # 管理员发表的评论
        comment= Comment(
            author='翟立元',
            email='01@lievenzhai.com',
            site='lievenzhai.com',
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            from_admin=True,
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
    db.session.commit()
    # 回复
    for i in range(salt):
        comment= Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            replied=Comment.query.get(random.randint(1, Comment.query.count())),
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)

