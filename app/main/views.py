from flask import render_template, request, redirect, url_for, abort
from . import main
from ..models import User,Pitch,Comments,Category,Votes
from .. import db
from . forms import PitchForm, CommentsForm, CategoryForm
from flask_login import login_required,current_user


#display categories on the landing page
@main.route('/')
def index():
    """ View root page function that returns index page """

    category = Category.get_categories()

    title = 'Home- Welcome'
    return render_template('index.html', title = title, categories=category)