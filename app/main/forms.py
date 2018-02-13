from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import Required

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about yourself', validators=[Required()])
    submit = SubmitField('Submit')

class BlogForm(FlaskForm):
    title = StringField("Caption",validators=[Required()])
    body = TextAreaField("Whats on your mind?", validators=[Required()])
    submit = SubmitField('Submit')