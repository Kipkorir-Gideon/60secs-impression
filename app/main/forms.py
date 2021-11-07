from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField
from wtforms.validators import Required


class PitchForm(FlaskForm):
    '''
    Class to create a wtf form for creating a pitch
    '''
    content = TextAreaField('Impress')
    submit = SubmitField('Submit')


class CommentsForm(FlaskForm):
    '''
    Class to create a wtf form for commenting a pitch
    '''
    comment = TextAreaField('Comment')
    submit = SubmitField('Submit')


class CategoryForm(FlaskForm):
    '''
    Class to create a wtf form for choosing a category 
    '''
    name =  StringField('Category Name', validators=[Required()])
    submit = SubmitField('Create')