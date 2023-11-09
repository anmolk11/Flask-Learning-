from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime
import math

def debug(*args):
    print('****************************')
    print(args)
    print('****************************')

with open('templates\config.json','r') as cfg:
    params = json.load(cfg)["params"]

local_server = True

app = Flask(__name__)
app.secret_key = params['secret_key']


if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['production_uri']
db = SQLAlchemy(app)

class Test(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(50))
    mobile = db.Column(db.String(50))
    email = db.Column(db.String(50))
    date = db.Column(db.String(50))
    slug = db.Column(db.String(50))

class Posts(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(50))
    content = db.Column(db.String(500))
    date = db.Column(db.String(50))
    slug = db.Column(db.String(50))

class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(50),unique = True,nullable = False)
    email = db.Column(db.String(500))
    password = db.Column(db.String(50))

@app.route("/")
def hello():
    name = 'Anmol bhai'
    return render_template('index.html',name = name)


@app.route("/posts")
def posts():
    _posts = Posts.query.filter_by().all()
    num_of_post = len(_posts)
    per_page = 3
    pages = math.ceil(num_of_post/per_page)
    page = request.args.get('page')
    # debug(page)
    # debug(num_of_post)

    if not page:
        page = 1
    else:
        page = int(page)
    
    if page == 1:
        prev = '#'
        next = '?page=' + str(page + 1)
    elif page == pages:
        prev = '?page=' + str(page - 1)
        next = '#'
    else:
        prev = '?page=' + str(page - 1)
        next = '?page=' + str(page + 1)
    
    start = (page - 1) * per_page

    return  render_template('test.html',posts = _posts[start : start + per_page],prev = prev,next = next)



@app.route("/posts/<string:slug_p>",methods = ['GET'])
def testing(slug_p):
    post = Posts.query.filter_by(slug = slug_p).first()
    return render_template('post.html',post = post)


@app.route("/base")
def base():
    return render_template('base.html')

@app.route("/form",methods = ['GET','POST'])
def form():
    if request.method == 'POST':
        _name = request.form.get('name') 
        _mobile = request.form.get('mobile') 
        _email = request.form.get('email') 
        _dob = request.form.get('dob') 

        entry = Test(name = _name,mobile = _mobile,email = _email,date = _dob)
        db.session.add(entry)
        db.session.commit()
    return render_template('form.html')




@app.route('/blog',methods = ['GET','POST'])
def blog_post():
    if request.method == 'POST':
        _title = request.form.get('blog-title')
        _content = request.form.get('blog-content')
        _date = datetime.now()
        _slug = '-'.join(_title.split(' '))
        entry = Posts(title = _title,content = _content,date = _date,slug = _slug)
        db.session.add(entry)
        db.session.commit()
    
    return render_template('blog.html')


@app.route('/login',methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        _username = request.form.get('username')
        _password = request.form.get('password')

        user = User.query.filter_by(username = _username).first()
        # debug(user) 
        if user and user.password == _password:
            # debug([_username,_password])
            return render_template('profile.html',user = user)
        else:
            return render_template('login.html',error = 'Invalid credentials')
    return render_template('login.html')    

@app.route('/signup',methods = ['GET','POST'])
def signup():
    if request.method == 'POST':
        _uname = request.form.get('user-name')
        _email = request.form.get('email')
        _password = request.form.get('password')

        print('\n\n\n I am here \n\n\n')

        entry = User(username = _uname,email = _email,password = _password)
        db.session.add(entry)
        db.session.commit()
        return render_template('login.html')
        
    return render_template('signup.html') 

@app.route('/profile')
def profile():
    return render_template('profile.html')    

app.run(debug = True)