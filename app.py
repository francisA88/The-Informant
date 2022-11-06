#By Francis Ali

from flask import render_template, redirect, Flask, request, abort
from flask_login import login_required, current_user,logout_user, login_user, LoginManager
import flask_login as fl

#from werkzeug.exceptions import HTTPException


from pathlib import Path
from datetime import datetime
import base64

from models import User, Blog, db
from helpers import *

BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__)
manager = LoginManager()
print(dir(manager))
manager.login_view = "/login-page"
manager.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{BASE_DIR}/db.sqlite3'
app.config['SECRET_KEY'] = base64.encodebytes(open('config').read().encode('utf-8')).decode('utf-8')

db.init_app(app)
print(dir(db.session))
#with app.app_context():
#	db.create_all()
@manager.user_loader
def load_user(user_id):
	with app.app_context():
		return User.query.get(user_id)
   
'''class Xdict(dict):

	def __getattribute__(self, attr):
		return super().get(attr)
		'''
class Views:
	@staticmethod
	def home():
		recents = Blog.query.order_by(Blog.date_created)
		context = {"recents":
			[{"title": b.title,
			  "content": b.content,
			  "author": b.user.username,
			  'date': f'{b.date_created.day} - {b.date_created.month} - {b.date_created.year}',
			  'blog_id': b.id} for b in recents.all()[::-1][:10]
			  ]
		}
		
		return render_template('index.html', **context)
		
	@staticmethod
	def view_blog(blog_id:int, slug:str):
		'''Do something here to get the blog details based on its `blog_id`.'''
		with app.app_context():
			blog = Blog.query.get(int(blog_id))
			if not blog:
				abort(404)
				if not (slug == slugify(blog.title)):
					abort(404)
				
		db.session.add(blog)
		date = blog.date_created
		recents = Blog.query.order_by(Blog.date_created)
		context = {
				'author': ([blog.user.fullname, blog.user.username][not bool(blog.user.fullname)]).title(), #Uses the Author's full name if available else the username is used.
				'date': f'{date.day} - {date.month} - {date.year}',
				'last_modified': None,
				'title': blog.title.title(),
				'content': blog.content,
				'blog_id': blog_id,
				"recents":
			[{"title": b.title,
			  "content": b.content,
			  "author": b.user.username,
			  'date': f'{b.date_created.day} - {b.date_created.month} - {b.date_created.year}',
			  'blog_id': b.id} for b in recents.all()[::-1][:10]
			  ]
		}
	#	db.session.close()
		return render_template('blog.html', **context)
		
	@staticmethod
	def login():
		'''Do login stuff with flask-login'''
		#Use csrftoken here too
		data = request.json
		username = data['username']
		user = User.query.filter_by(username=username).first()
		password = data['password']
		if user:
			if get_hash_string_SHA256(password) == user.password:
				login_user(user, remember=True)
				print(current_user)
				return redirect("/dashboard")
		return {"status": 401}
		
	@staticmethod
	def create_blog():
		data = request.json
		#csrf_token = request.headers.get("X-CSRF-Token")
#		if not (csrf_token and is_csrf_validated(csrf_token)):
#			abort(401) #Not sure if this is right.
		blog_content = data['content']
		blog_title = data['title']
		try:
			with app.app_context():
				blog = Blog(content=blog_content, title=blog_title, user=current_user, date_created=datetime.now())
				db.session.add(blog)
				db.session.commit()
			return {'status': 201}
		except Exception as e:
			return {'status': '500'}
		
	@staticmethod
	@login_required
	def creation_page():
		return render_template("create.html")
		
	@staticmethod
	def login_page():
		if current_user.is_authenticated:
			return redirect('/dashboard')
		return render_template('login.html')
	@staticmethod
	def contact_page():
		return render_template('contact.html')
	@staticmethod
	def signup_page():
		return render_template('signup.html')
	@staticmethod
	def signup():
		#Use csrftoken here too
		data = request.json
		username = data["username"]
		fullname = data['fullname']
		email = data['email']
		password = get_hash_string_SHA256(data['password'])
		with app.app_context():
			new_user = User(username=username, fullname=fullname, email=email, password=password)
			db.session.add(new_user)
			db.session.commit()
			login_user(new_user, remember=True)
			return {"status": 201}
		return {"status": 401}
		
	@staticmethod
	@login_required
	def save_changes(blog_id:int):
		'''Save changes made after editing a blog'''
		#Requires login
		#Use csrf token here too
		with app.app_context():
			blog = Blog.query.get(int(blog_id))
			data = request.json
			modified_content = data['content']
			modified_title = data['title']
			blog.title = modified_title
			blog.content = modified_content
			db.session.commit()
		return {'status': 201}
		
	@staticmethod
	def edit_blog(blog_id:int):
		with app.app_context():
			blog = Blog.query.get(blog_id)
			if not blog:
				abort(404)
				if blog.user.username != current_user.username:
					abort(401)
			
		return render_template("edit.html", 
			**{
				"blog_id": blog_id,
				"slug": slugify(blog.title),
			})
		
	@staticmethod
	@login_required
	def dashboard():
		with app.app_context():
			print(current_user)
			blogs_for_user = Blog.query.filter_by(user=current_user).first()
			context = {"blogs":[], 'user': current_user}
			if blogs_for_user:
				for blog in blogs_for_user:
					date = blog.date_created
					context["blogs"].append({
						'id': blog.id,
						'title':  blog.title,
						'date': f'{date.day} - {date.month} - {date.year}',
					})
		return render_template("dashboard.html", **context)
		
	@staticmethod
	@login_required
	def logout():
		logout_user()
		return redirect('/')

from datetime import datetime
def _create_blog(user, title, content):
	with app.app_context():
		blog = Blog(user=user, title=title, content=content, date_created=datetime.now())
		db.session.add(blog)
		db.session.commit()
	
urls = [
	('/',  Views.home),
	('/blogs/<int:blog_id>/view/<slug>', Views.view_blog),
	('/blogs/create', Views.create_blog, ['POST']),
	('/creation-page', Views.creation_page),
	('/contact-us', Views.contact_page),
	('/login-page', Views.login_page),
	('/signup-page', Views.signup_page),
	('/login', Views.login, ["POST"]),
	('/signup', Views.signup, ['POST']),
	('/dashboard', Views.dashboard),
	('/blogs/<int:blog_id>/edit', Views.edit_blog),
	('/blogs/<int:blog_id>/save', Views.save_changes, ["POST"]),
	('/logout', Views.logout)
]
#few configurations for the app's running
settings = {
	"debug": True,
	#...
}
if __name__ == '__main__':
	map_urls(app, urls)
	app.run(**settings)