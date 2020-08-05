from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, DateField, BooleanField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError, Email, URL, Optional
from flask_ckeditor import CKEditorField
from thirty_man.models import Category


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    password = StringField('Password', validators=[DataRequired(), Length(1, 128)])
    remember = BooleanField('Remember me')
    submit = SubmitField()


class PostForm(FlaskForm):
    title = StringField('Tile', validators=[DataRequired(), Length(1, 60)])
    category = SelectField('Category', coerce=int, default=1)
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField()

    def __init__(self):
        super(PostForm, self).__init__()
        self.category.choices = [(category.id, category.name) for category in Category.query.order_by(Category.name).all()]


class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    submit = SubmitField()

    def validate_name(self, field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError('分类名已存在')


class CommentForm(FlaskForm):
    author = StringField('Author', validators=[DataRequired(), Length(1, 30)])
    email = StringField('Email', validators=[DataRequired(), Length(1, 254), Email()])
    site = StringField('Site', validators=[URL(), Length(0, 255), Optional()])
    body = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField()


class AdminCommentForm(CommentForm):
    author = HiddenField()
    emial = HiddenField()
    site = HiddenField()


class LinkForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(1, 30)])
    url = StringField('url', validators=[DataRequired(), URL(), Length(1, 255)])
    submit = SubmitField()




class SettingForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    blog_title = StringField('Blog Title', validators=[DataRequired(), Length(1, 60)])
    blog_sub_title = StringField('Blog Sub Title', validators=[DataRequired(), Length(1, 100)])
    about = CKEditorField('About Page', validators=[DataRequired()])
    submit = SubmitField()
