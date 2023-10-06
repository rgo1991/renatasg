from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from main import db
from main.models import Post
from main.posts.forms import PostForm
from flask import Blueprint

posts = Blueprint('posts', __name__)

@posts.route("/post/new", methods=['GET', 'POST']) #create_post.html template is rendered when this route is accessed.
@login_required #cannot access this route unless user is logged in.
def new_post():
    form = PostForm() #initialize the PostForm class
    if form.validate_on_submit(): #check if all the entered data in the form passes the validation checks that are outlined in the class 
        post = Post(title=form.title.data, content=form.content.data, author=current_user) #if validation passes create a object using Post() class with the values entered by user
        db.session.add(post) #add changes to database
        db.session.commit() #commit changes to database
        flash('Your Post has been submited', 'success') #send flash message to user 
        return redirect(url_for('main.home')).posts #redirect user to home page at the end
    return render_template('create_post.html', title='New Post', form=form, legend='New Post') #render the new post template when route is accessed.


@posts.route("/post/<int:post_id>") #link for when user clicks into the actual post. Displays only single post
def post(post_id): #takes post_id as argument
    post = Post.query.get_or_404(post_id) #if post id doesnt exist, then give 404
    return render_template('post.html', title=post.title, post=post) # render tamplate with the contents 


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])  
@login_required
def update_post(post_id): 
    post = Post.query.get_or_404(post_id)
    if post.author != current_user: # if the post.author doesnt equal the current_user value (imported above) then cant update post and need to avort with 403
        abort(403)
    form = PostForm() # create a form object
    if form.validate_on_submit(): #confirm if form validates the input
        post.title = form.title.data # update db value for post.title with the data entered in the form
        post.content = form.content.data # update db value for post.content with the content in the form
        db.session.commit() #commit db changes
        flash('Your Post has been updated', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET': # fills in the content of the rendered form with the current values for title and content for this post, ready for editing.  
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post) #delete post in db
    db.session.commit()
    flash('Your Post has been deleted', 'success')
    return redirect(url_for('main.home'))
