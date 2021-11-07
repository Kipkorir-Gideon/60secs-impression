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
    ''' 
    Function to check Pitches form and fetch data from the fields
    '''
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


@main.route('/add/category', methods=['GET','POST'])
@login_required
def new_category():
    '''
    View new group route function that returns a page with a form to create a category
    '''
    form = CategoryForm()

    if form.validate_on_submit():
        name = form.name.data
        new_category = Category(name=name)
        new_category.save_category()

        return redirect(url_for('.index'))

    title = 'New category'
    return render_template('new_category.html', category_form = form,title=title)



#A route for adding a comment
@main.route('/write_comment/<int:id>', methods=['GET', 'POST'])
@login_required
def post_comment(id):
    ''' function to post comments '''
    form = CommentsForm()
    title = 'post comment'
    pitches = Pitch.query.filter_by(id=id).first()

    if pitches is None:
         abort(404)

    if form.validate_on_submit():
        opinion = form.opinion.data
        new_comment = Comments(opinion=opinion, user_id=current_user.id, pitches_id=pitches.id)
        new_comment.save_comment()
        return redirect(url_for('.view_pitch', id=pitches.id))

    return render_template('post_comment.html', comment_form=form, title=title)



#view single pitch alongside its comments
@main.route('/view-pitch/<int:id>', methods=['GET', 'POST'])
@login_required
def view_pitch(id):
    '''
    Function the returns a single pitch for comment to be added
    '''
    print(id)
    pitches = Pitch.query.get(id)
    # pitches = Pitch.query.filter_by(id=id).all()

    if pitches is None:
        abort(404)
    #
    comment = Comments.get_comments(id)
    return render_template('view-pitch.html', pitches=pitches, comment=comment, category_id=id)