
import mysql.connector
from flask import Flask, render_template, request, url_for,flash, redirect
from werkzeug.exceptions import abort
from post import Post
import secrets, datetime

app = Flask(__name__)
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
    mycursor.execute('SELECT * FROM post WHERE id =%s',
(post_id,))
    row = mycursor.fetchone()  
    myconn.close()
    if row is None:
        abort(404)
    else:
        post = Post(row['id'], row['created'], row['title'],
row['content'])
        return post

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)
    
@app.route('/create', methods=('GET', 'POST'))
def create():
    return render_template('create.html')
