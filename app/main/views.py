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


#Route for adding a new pitch
@main.route('/category/new-pitch/<int:id>', methods=['GET', 'POST'])
@login_required
def pitch(id):
    ''' Function to check Pitches form and fetch data from the fields '''
    form = PitchForm()
    category = Category.query.filter_by(id=id).first()

    if category is None:
        abort(404)

    if form.validate_on_submit():
        content = form.content.data

        # Updated pitch instance
        pitch= Pitch(content=content,category_id= category.id,user_id=current_user.id)

        # save pitch method
        pitch.save_pitch()
        return redirect(url_for('.category', id=category.id))

    return render_template('pitch.html', pitch_form=form, category=category)


#A route to display pitches of a specific category
@main.route('/categories/<int:id>')
def category(id):
    category = Category.query.get(id)
    if category is None:
        abort(404)

    pitches=Pitch.get_pitches(id)
    return render_template('category.html', pitches=pitches, category=category)