from flask import Flask, render_template


# Create a Flask Instance - It will be running and does all the things

app = Flask(__name__)  # __name__ helps to find all our files in our directory

app.debug=True


# Crate a route decorator

@app.route('/')  # app the above one and in route is the route | / represents home page

# def index():
	# return "<h1>Hello World!</h1>"

# FILTERS !!!
# safe - implement tags
# capitalize
# upper
# title - makes first letter capital 
# trim - remove spacs
# striptags - ignore tags

def index():
	first_name = "John"
	stuff = "This is <strong> Bold</strong> text"
	favorite_pizza=['Pepperoni', 'Cheese', 'Mushrooms', 41]
	return render_template("index.html",
		first_name=first_name,
		stuff = stuff,
		favorite_pizza=favorite_pizza)





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

















