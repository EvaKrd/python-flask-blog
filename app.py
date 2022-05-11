
import mysql.connector
from flask import Flask, render_template, request, url_for,flash, redirect
from werkzeug.exceptions import abort
from post import Post
import secrets, datetime
from flask_login import LoginManager

login_manager = LoginManager()
app = Flask(__name__)
login_manager.init_app(app)
app.config['SECRET_KEY'] = secrets.token_hex(16)
@app.route('/')
def index():    
    myconn = get_db_connection()
    mycursor = myconn.cursor(dictionary=True)
    mycursor.execute('SELECT id, created, title, content FROM post')
    rows = mycursor.fetchall()
    myconn.close()
    posts = []
    for row in rows:
        post = Post(row['id'], row['created'] , row['title'], row['content'])
        posts.append(post)
    return render_template('index.html', posts=posts)
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="python-flask-blog",
            password="YEmuCebo13",
            database="python-flask-blog"
        )
        return connection
        

    except mysql.connector.Error as e:
        print(e)

def get_post(post_id):
    myconn = get_db_connection()
    mycursor = myconn.cursor(dictionary=True)
    mycursor.execute('SELECT * FROM post WHERE id =%s', (post_id,))
    row = mycursor.fetchone()  
    myconn.close()
    if row is None:
        abort(404)
    else:
        post = Post(row['id'], row['created'], row['title'], row['content'])
        return post

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)
    
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            myconn = get_db_connection()
            mycursor = myconn.cursor(dictionary=True)
            mycursor.execute('INSERT INTO post (created, title, content) VALUES (%s, %s, %s)', (datetime.datetime.now(), title, content))
            myconn.commit()
            myconn.close()
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            flash('Title is required!')
        else:
            myconn = get_db_connection()
            mycursor = myconn.cursor(dictionary=True)
            mycursor.execute('UPDATE post SET title = %s, content = %s WHERE id = %s',  (title, content, id))
            myconn.commit()
            myconn.close()
            return redirect(url_for('index'))
    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    myconn = get_db_connection()
    mycursor = myconn.cursor(dictionary=True)
    mycursor.execute('DELETE FROM post WHERE id = %s', (id,))
    myconn.commit()
    myconn.close()
    flash('"{}" was successfully deleted!'.format(post.title))
    return redirect(url_for('index'))
    
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        login_user(user)

        flask.flash('Logged in successfully.')

        next = flask.request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        if not is_safe_url(next):
            return flask.abort(400)

        return flask.redirect(next or flask.url_for('index'))
    return flask.render_template('login.html', form=form)
