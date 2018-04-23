
from flask import Flask, request, redirect, render_template,session,flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

app.secret_key = 'haleofidjakn303'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(12))
    blogs = db.relationship('Blog',backref = 'owner')
    #Need to add property tying this to Blog class

    def __init__(self,username,password):
        self.username=username
        self.password=password

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))
    
    owner_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    def __init__(self, title,body):
        self.title = title
        self.body = body
       

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup','index','allblogs','misterindex','']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/newpost')
        if (not username) or (username.strip() == ""):
            flash("Oops, you didn't enter a username",'error')
        else:
            flash('User password incorrect, or user does not exist', 'error')

    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        # TODO - validate user's data
        username_error = ''
        password_error = ''
        verify_error = ''

        if (not username) or (username.strip() == ""):
            flash("That's not a valid username","error")
            username_error = "Not a valid username"
            username = ''
            password = ''
            verify = ''
        else:
            if len(username) > 20 or len(username) < 3:
                flash("That username is too short/long","error")
                username_error = "That username is too short/ long"
                username = ''
                password= ''
                verify = ''
    
        if (not password) or (password.strip() == ""):
            flash("Not a valid password","error")
            password_error = "Not a valid password"
            password = ''
        else:
            if len(password) > 20 or len(password) <3:
                flash("That password is too short/long","error")
                password_error = "That password is too long/short"
                password = ''
    
        if (not verify) or (verify.strip() == ""):
            flash("That's not a valid verify password","error")
            verify_error = "That's not a valid password"
            verify = ''
            password = ''
        if verify != password:
            flash("Oops, your passwords don't match","error")
            verify_error = "Oops, your passwords don't match."
            verify = ''
            password = ''


        existing_user = User.query.filter_by(username=username).first()
        if not existing_user and not username_error and not password_error and not verify_error:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
        else:
            flash("That username has already been used","error")
            return render_template('signup.html')

    return render_template('signup.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')



@app.route('/allblogs', methods = ['POST','GET'])
def index():

    blogs = Blog.query.all()
    user = User.query.all()
    
    return render_template('index.html',blogs=blogs,user=user)


@app.route('/',methods = ['POST','GET'])
def misterindex():

    user = User.query.all()

    return render_template('buildablog.html',user=user)


@app.route('/newpost', methods = ['POST','GET'])
def newpost():
    #Need to edit this handler due to the new parameter
    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_body = request.form['blog_body']
        error_title = ""
        error_body = ""
        if (not blog_title) or (blog_title.strip() == ""):
            error_title = "Add a title ya dummy!"
        if (not blog_body) or (blog_body.strip() == ""):
            error_body = "Add a body ya dummy!"
        if not error_body and not error_title:
            new_blog = Blog(blog_title,blog_body)
            db.session.add(new_blog)
            db.session.commit()
            url = './singleblog?id=' + str(new_blog.id)
            return redirect(url)
        else:
            return render_template('newpost.html',error_body = error_body, error_title = error_title)
    else:
        return render_template('newpost.html')
        

@app.route('/singleblog',methods = ['POST','GET'])
def singleblog():
    blog_id = request.args.get('id')
    if (blog_id):
        blog = Blog.query.get(blog_id)
        return render_template('singleblog.html',blog = blog)




if __name__ == '__main__':
    app.run()