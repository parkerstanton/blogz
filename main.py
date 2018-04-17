
from flask import Flask, request, redirect, render_template,session,flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))

    def __init__(self, title,body):
        self.title = title
        self.body = body


@app.route('/', methods = ['POST','GET'])
def index():

    blogs = Blog.query.all()
    return render_template('buildablog.html',blogs=blogs)




@app.route('/newpost', methods = ['POST','GET'])
def newpost():

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