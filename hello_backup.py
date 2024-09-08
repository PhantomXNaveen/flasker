from flask import Flask, render_template, flash, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.widgets import TextArea
from flask_login import login_user, current_user, logout_user, login_required, UserMixin, LoginManager

# Create a Flask Instance - It will be running and does all the things
app = Flask(__name__)  # __name__ helps to find all our files in our directory

# Add Database
# SQLite DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# MYSQL DB
# app.config['SQLALCHEMY_DATABASE_URI']='mysql://username:password@localhost/db_name'
# app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@localhost/our_users'
# Secret Key!
app.config['SECRET_KEY'] = "UNKNOWN" # For WTF fomrs

# Initialize The Database
db = SQLAlchemy(app)
# Migration
migrate = Migrate(app,db)

# Json Thing
@app.route('/date')
def get_current_date():
	favorite_pizza = {
	"John": "Pepperoni",
	"Mary": "Cheese",
	"Tim": "Mushroom"
	}
	return favorite_pizza
	# return {"Date": date.today()}

# Create a Blog Post Model
class Posts(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	title=db.Column(db.String(255))
	content=db.Column(db.Text)
	author=db.Column(db.String(255))
	date_posted=db.Column(db.DateTime, default=datetime.utcnow) 
	slug= db.Column(db.String(255))   

# Create a Model
class Users(db.Model, UserMixin):
	id=db.Column(db.Integer,primary_key=True)
	username=db.Column(db.String(20),unique=True,nullable=False)
	name=db.Column(db.String(150),nullable=False)
	email=db.Column(db.String(100),unique=True,nullable=False)
	favorite_color=db.Column(db.String(80))
	date_added=db.Column(db.DateTime,default=datetime.utcnow)
	# Do Some Password Stuff!
	password_hash=db.Column(db.String(128))

	@property
	def password(self):
		raise AttributeError ('password is not a readable attribute')
	
	@password.setter
	def password(self,password):
		self.password_hash=generate_password_hash(password)

	def verify_password(self,password):
		return check_password_hash(self.password_hash,password)

	# Create a String
	def __repr__(self):
		return '<Name %r>' % self.name


# Flask_Login stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
	return Users.query.get(int(user_id))


# Create a User Form Class
class UserForm(FlaskForm):
	name = StringField("Name",validators=[DataRequired()])
	username = StringField("UserName",validators=[DataRequired()])
	email = StringField("Email",validators=[DataRequired()])
	favorite_color=StringField("Favorite Color")
	password_hash = PasswordField('Password', validators=[DataRequired(),EqualTo('password_hash2',message = 'Passwords Must Match!')])
	password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
	submit = SubmitField("Submit") 

# Create a PostForm
class PostForm(FlaskForm):
	title = StringField("Title",validators=[DataRequired()])
	content = StringField("Content",validators=[DataRequired()],widget=TextArea())
	author = StringField("Author",validators=[DataRequired()])
	slug = StringField("Slug",validators=[DataRequired()])
	submit = SubmitField("Submit")

# Create a Form Class
class NamerForm(FlaskForm):
	name = StringField("What's your name?",validators=[DataRequired()])
	submit = SubmitField("Submit") 


# Create a Password Form 
class PasswordForm(FlaskForm):
	email = StringField("What's your email?",validators=[DataRequired()])
	password_hash = PasswordField("What's your password?",validators=[DataRequired()])
	submit = SubmitField("Submit") 


# Create a Login Form
class LoginForm(FlaskForm):
	username = StringField("UserName",validators=[DataRequired()])
	password = PasswordField("Password",validators=[DataRequired()])
	submit = SubmitField("Submit")


# Create a Login Page
@app.route('/login',methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(username=form.username.data).first()
		if user:
			# Check the hash
			if check_password_hash(user.password_hash, form.password.data):
				login_user(user)
				flash("Login Successful !!!")
				return redirect(url_for('dashboard'))
			else:
				flash("Wrong Password - Try Again")
		else:
			flash("That User doesn't Exist! Try Again!! ")			
	return render_template('login.html',form=form)


# Create a Dashboard Page
@app.route('/dashboard',methods=['GET','POST'])
@login_required
def dashboard():
	id = current_user.id
	form = UserForm()	
	name_to_update = Users.query.get_or_404(id)
	if request.method == "POST":
		name_to_update.name = request.form['name']
		name_to_update.email = request.form['email']
		name_to_update.favorite_color = request.form['favorite_color']
		name_to_update.username = request.form['username']
		try:
			db.session.commit()
			flash("User Updated Successfully")
			return render_template("dashboard.html",
				form=form,
				name_to_update=name_to_update)
		except:
			flash("Error! Something Went Wrong")
			return render_template("dashboard.html",
			form=form,
			name_to_update=name_to_update)		
	else:	
		return render_template("dashboard.html",
		form=form,
		id = id,
		name_to_update=name_to_update)
	return render_template('dashboard.html')


# Create a Logout Page
@app.route('/logout',methods=['GET','POST'])
@login_required
def logout():
	logout_user()
	flash("You Have Been Logged Out. Thanks for visiting..")
	return redirect(url_for('login'))


	# BooleanField
	# DateField
	# DateTimeField
	# DecimalField
	# FileField
	# HiddenField
	# MultipleField
	# FieldList
	# FloatField
	# FormField
	# IntegerField
	# PasswordField
	# RadioField
	# SelectField
	# SelectMultipleField
	# SubmitField
	# StringField
	# TextAreaField

	
	## Validators

	# DataRequired
	# Email
	# EqualTo
	# InputRequired
	# IPAddress
	# Length
	# MacAddress
	# NumberRange
	# Optional
	# Regexp
	# URL
	# UUID
	# AnyOf
	# NoneOf


# FILTERS !!!
# safe - implement tags
# capitalize
# upper
# title - makes first letter capital 
# trim - remove spacs
# striptags - ignore tags


# Create a route decorator
@app.route('/')  # app the above one and in route is the route | / represents home page
def index():
	# return "<h1>Hello World!</h1>"
	flash("Welcome to Our WebPage")
	first_name = "John"
	stuff = "This is <strong> Bold</strong> text"
	favorite_pizza=['Pepperoni', 'Cheese', 'Mushrooms', 41]
	return render_template("index.html",
		first_name=first_name,
		stuff = stuff,
		favorite_pizza=favorite_pizza)


@app.route('/user/add',methods=['GET','POST'])
def add_user():
	name = None
	form = UserForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(email=form.email.data).first()
		if user is None:
			# Hash the Password
			hashed_pw = generate_password_hash(form.password_hash.data, method="pbkdf2:sha256")
			user = Users(name=form.name.data,username =form.username.data,email=form.email.data,favorite_color=form.favorite_color.data,password_hash=hashed_pw)
			db.session.add(user)
			db.session.commit()
		name = form.name.data
		form.name.data = ''
		form.username.data=''
		form.email.data= ''
		form.favorite_color.data=''
		form.password_hash=''
		flash("User Added Successfully!")
	our_users = Users.query.order_by(Users.date_added)		
	return render_template("add_user.html",
		form = form,
		name = name,
		our_users=our_users)


# Delete Database Record
@app.route('/delete/<int:id>',methods = ['GET','POST'])
def delete(id):
	user_to_delete = Users.query.get_or_404(id)
	name = None
	form = UserForm()
	try:
		db.session.delete(user_to_delete)
		db.session.commit()
		flash('User Deleted Successfully!!')
		our_users = Users.query.order_by(Users.date_added)		
		return render_template("add_user.html",
		form = form,
		name = name,
		our_users=our_users)		

	except:
		flash("Whoops! An error occurred")
		return render_template("add_user.html",
		form = form,
		name = name,
		our_users=our_users)


# Update Database Record
@app.route('/update/<int:id>',methods = ['GET','POST'])
def update(id):
	form = UserForm()
	name_to_update = Users.query.get_or_404(id)
	if request.method == "POST":
		name_to_update.name = request.form['name']
		name_to_update.email = request.form['email']
		name_to_update.favorite_color = request.form['favorite_color']
		name_to_update.username = request.form['username']
		try:
			db.session.commit()
			flash("User Updated Successfully")
			return render_template("update.html",
				form=form,
				name_to_update=name_to_update)
		except:
			flash("Error! Something Went Wrong")
			return render_template("update.html",
			form=form,
			name_to_update=name_to_update)		
	else:	
		return render_template("update.html",
		form=form,
		id = id,
		name_to_update=name_to_update)	


# localhost:5000/user/John
@app.route('/user/<name>') 
# The route will look like as mentioned above
def user(name):
	# return "<h1>Hello {}!!</h1>".format(name)
	return render_template("user.html",user_name=name)


# Create Custom Error Pages

# Inavalid URL
@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404


# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
	return render_template("500.html"), 500


# Create Password Test Page 
@app.route('/test_pw', methods=['GET','POST'])	
def test_pw():
	email = None
	password = None
	pw_to_check = None
	passed = None
	form = PasswordForm()
	# Validate Form
	if form.validate_on_submit():
		email = form.email.data
		password = form.password_hash.data
		# Clear the Form
		form.email.data =''
		form.password_hash.data =''
		
		# Lookup User By Email Address
		pw_to_check = Users.query.filter_by(email=email).first()
		
		# Check Hashed Password
		passed = check_password_hash(pw_to_check.password_hash,password)
	return render_template("test_pw.html",
		email = email,
		password = password,
		pw_to_check=pw_to_check,
		passed = passed,
		form = form)


# Add Post Page
@app.route('/add-post', methods=['GET','POST'])
# @login_required | Check out if else statement used to lockdown the app 
def add_post():
	form = PostForm()

	if form.validate_on_submit():
		post = Posts(title=form.title.data, content=form.content.data, author=form.author.data, slug=form.slug.data)
		# Clear the Form
		form.title.data=''
		form.content.data=''
		form.author.data=''
		form.slug.data=''

		# Add post data to database 
		db.session.add(post)
		db.session.commit()

		# Flash message
		flash("Blog Post Submitted Successfully!")

	# Redirect to Webpage
	return render_template("add_post.html",form = form)

@app.route('/posts/delete/<int:id>')
def delete_post(id):
	post_to_delete = Posts.query.get_or_404(id)

	try:
		db.session.delete(post_to_delete)
		db.session.commit()
		# Return a Flash Page
		flash("Blog Post was Deleted")
		# Grab all the posts from the database
		posts = Posts.query.order_by(Posts.date_posted)	
		return render_template('posts.html',posts= posts)
	except:
		# Return an Error message
		flash("Whoops! Failure occurred")

		# Grab all the posts from the database
		posts = Posts.query.order_by(Posts.date_posted)	
		return render_template('posts.html',posts = posts)

@app.route('/posts')
def posts():
	# Grab all the posts from the databases
	posts = Posts.query.order_by(Posts.date_posted)
	return render_template("posts.html",posts=posts)

@app.route('/post/<int:id>')
def post(id):
	post = Posts.query.get_or_404(id)
	return render_template('post.html',post = post)

@app.route('/posts/edit/<int:id>',methods = ['GET','POST'])
@login_required
def edit_post(id):
	post = Posts.query.get_or_404(id)
	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		post.author = form.author.data
		post.slug = form.slug.data
		post.content = form.content.data
		# Update Database
		db.session.add(post)
		db.session.commit()
		# Flash message
		flash("Post has been Updated!")
		return redirect(url_for('post',id=post.id))
	form.title.data = post.title
	form.author.data= post.author
	form.slug.data = post.slug
	form.content.data = post.content
	return render_template('edit_post.html',form=form)



# Create Name page , Post the form in bcknd Get a web page
@app.route('/name', methods=['GET','POST'])	
def name():
	name = None
	form = NamerForm()
	# Validate From
	if form.validate_on_submit():
		name = form.name.data
		form.name.data =''
		flash("Form Submitted Successfully")
	return render_template("name.html",
		name = name,
		form = form)


@app.route('/test')
def test():
	return render_template('test.html')


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Users': Users}


if __name__ == '__main__':
    app.run(debug=True)   















