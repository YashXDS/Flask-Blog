from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import json
from datetime import datetime
from itsdangerous import URLSafeTimedSerializer
import os
from werkzeug.utils import secure_filename
import math

with open("config.json", "r") as c:
    params = json.load(c)["params"]
    
app = Flask(__name__)
app.secret_key = "yash-patel"
app.config['UPLOAD_FOLDER'] = params['file_path']

# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True
# app.config['MAIL_USERNAME'] = params["gmail-user"]
# app.config['MAIL_DEFAULT_SENDER'] = params["gmail-user"]
# app.config['MAIL_PASSWORD'] = params["gmail-password"]
# mail = Mail(app)

local_server = True
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params["local_uri"]
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params["prod_uri"]
    
db = SQLAlchemy(app)

class Contact(db.Model):
    index = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), nullable = False)
    Email = db.Column(db.String(25), nullable = False)
    Phone = db.Column(db.String(15), nullable = False)
    Message = db.Column(db.String(150), nullable = False)
    Date = db.Column(db.String(12), nullable = True)

class Posts(db.Model):
    index = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable = False)
    tagline = db.Column(db.String(200), nullable = False)
    slug = db.Column(db.String(30), nullable = False)
    content = db.Column(db.String(200), nullable = False)
    date = db.Column(db.String(120), nullable = True)
   

@app.route("/")
def home():
    posts = Posts.query.filter_by().all()
    last = math.ceil(len(posts)/int(params['no_of_posts']))
    #[0: params['no_of_posts']]
    #posts = posts[]
    page = request.args.get('page')
    if(not str(page).isnumeric()):
        page = 1
    page= int(page)
    posts = posts[(page-1)*int(params['no_of_posts']): (page-1)*int(params['no_of_posts'])+ int(params['no_of_posts'])]
    #Pagination Logic
    #First
    if (page==1):
        prev = "#"
        next = "/?page="+ str(page+1)
    elif(page==last):
        prev = "/?page=" + str(page - 1)
        next = "#"
    else:
        prev = "/?page=" + str(page - 1)
        next = "/?page=" + str(page + 1)



    return render_template('index.html', params=params, posts=posts, prev=prev, next=next)

@app.route("/about")
def about():
    return render_template('about.html', params=params)

@app.route("/admin", methods = ['GET', 'POST'])
def admin():
    if 'user' in session and session['user'] == params['admin_name']:
        posts = Posts.query.all()

        return render_template("admin.html", params = params, posts = posts)
    
    if request.method == 'POST':
        umail = request.form.get("email")
        upassword = request.form.get("pass")
        if (umail == params['admin_name'] and upassword == params['admin_password']):
            session['user'] = umail
            posts = Posts.query.all()
            return render_template("admin.html", params = params, posts = posts)     
    return render_template('login.html', params=params)

@app.route("/uploader", methods=['POST'])
def uploader():
    if 'user' in session and session['user'] == params['admin_name']:
        if request.method == 'POST':
            f = request.files['file1']
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            return "Uploaded Successfully"
        
@app.route("/logout")
def logout():
    session.pop('user')
    return redirect("/admin")
        
@app.route("/post/<string:post_slug>", methods = ["GET"])
def post_route(post_slug):
    post =  Posts.query.filter_by(slug = post_slug).first()
    return render_template('post.html', params=params, post = post)

@app.route("/add", methods = ["GET","POST"])
def add():
    if 'user' in session and session['user'] == params['admin_name']:
        if request.method == 'POST':
            a_title = request.form.get('title')
            a_tagline = request.form.get('tagline')
            a_slug = request.form.get('slug')
            a_content = request.form.get('content')
            a_date = datetime.now()
            post = Posts(title = a_title, tagline = a_tagline, slug = a_slug, content = a_content, date = a_date) 
            db.session.add(post)
            db.session.commit()
        return render_template('add.html', params=params)      

@app.route("/edit/<string:index>", methods = ["GET","POST"])
def edit(index):
    if 'user' in session and session['user'] == params['admin_name']:
        if request.method == 'POST':
            e_title = request.form.get('title')
            e_tagline = request.form.get('tagline')
            e_slug = request.form.get('slug')
            e_content = request.form.get('content')
            e_date = datetime.now()
            post = Posts.query.filter_by(index = index).first()
            post.title = e_title
            post.tagline = e_tagline
            post.slug = e_slug
            post.content = e_content
            post.date = e_date
            db.session.commit()
            return redirect("/admin")
        post = Posts.query.filter_by(index = index).first()
        return render_template('edit.html', params=params, post = post)  
    
@app.route("/delete/<string:index>", methods = ["GET","POST"])
def delete(index):
     if 'user' in session and session['user'] == params['admin_name']:
         post = Posts.query.filter_by(index=index).first()
         db.session.delete(post)
         db.session.commit()
         return redirect("/admin")
         
   
@app.route("/contact", methods = ["GET","POST"])  # Allow both GET and POST
def contact():
    if(request.method == "POST"): 
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message') 
        entry = Contact(Name=name, Email=email, Phone=phone, Message=message,  Date=datetime.now()) 
        db.session.add(entry)
        db.session.commit()
        # mail.send_message(sender = email,
        #                   recipients = params["gmail-user"],
        #                   body = message + "\n" + phone 
            
        #                 )
        return redirect("/")
    return render_template('contact.html', params=params)

app.run(debug=True)