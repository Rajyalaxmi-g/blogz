from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
#create connection string which connects to db
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:root@localhost:8889/build-a-blog'

app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app) 

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blog_title = db.Column(db.String(120))
    blog_post = db.Column(db.String(120))

    def __init__(self, blog_title,blog_post):
        self.blog_title = blog_title
        self.blog_post = blog_post

@app.route('/blog', methods=['GET'])
def blogid():
    id = request.args.get('id')
    if id is None:
        blogs = Blog.query.all()
        return render_template("mainblog.html", blogs = blogs)
    else:

        print("our id = " , id)
        indi_post = Blog.query.filter_by(id=id).first()
        print("individual = " ,indi_post.blog_title,indi_post.blog_post)
    return render_template('individualpost.html',indi_post=indi_post)



@app.route('/newpost', methods=['POST','GET'])
def new_post():

    if request.method == 'POST':
        new_blogtitle = request.form['newblogtitle']
        new_blog = request.form['newblog']
        blogtitle_error = ""
        blogbody_error = ""
        
        
        if new_blogtitle == "" or new_blog == "":
            blogtitle_error = "Please fill in the title"
            blogbody_error = "Please fill in the body"
                       
            return render_template('post_newblog.html',title_error=blogtitle_error,body_error=blogbody_error)

        else:      
            new_blogs = Blog(new_blogtitle, new_blog)
            #db.session.add(new_blogs)
            print("constructor=",new_blogs)
            print("add= ",db.session.add(new_blogs))
            print("commit= ",db.session.commit())
            id = new_blogs.id
            print("id value = ", id)
            return redirect('/blog?id='+ str(id))

               
    return render_template('post_newblog.html')


if __name__ == '__main__':
    app.run()