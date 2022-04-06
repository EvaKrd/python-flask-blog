import mysql.connector
from flask import Flask, render_template
from post import Post

app = Flask(__name__)
@app.route('/')
def index():    
    myconn = get_db_connection()
    mycursor = myconn.cursor(dictionary=True)
    mycursor.execute('SELECT id, created, title, content FROM post')
    rows = mycursor.fetchall()
    myconn.close()
    posts = []
    for row in rows:
        post = Post(row['id'], row['title'], row['content'])
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