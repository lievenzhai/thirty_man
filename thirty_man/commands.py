import click
from thirty_man.extensions import db


def register_commands(app):
    @app.cli.command()
    @click.option('--category', default=10, help='分类的数量，默认是10')
    @click.option('--post', default=50)
    @click.option('--comment', default=500)
    def forge(category, post, comment):
        '''生成虚拟的分类、文章和评论'''
        from thirty_man.fakes import fake_posts, fake_categories, fake_comment, fake_admin
        db.drop_all()
        db.create_all()

        click.echo('生成管理员账户')
        fake_admin()

        click.echo('生成%d条分类' % category)
        fake_categories()

        click.echo('生成%d篇文章' % post)
        fake_posts()

        click.echo('生成%d条评论' % comment)
        fake_comment()

        click.echo('完成')