from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

#from flask import Flask

db = SQLAlchemy()
print(1)

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), unique=True, nullable=False)
	email = db.Column(db.String(50), unique=True, nullable=False)
	password = db.Column(db.String(500), nullable=False)
	fullname = db.Column(db.String(100), nullable=True)
	
	def __repr__(self):
		return self.username
	
	def create(self):
		db.session.add(self)
		db.session.commit()
		
	def delete(self):
		db.session.delete(self)
		db.session.commit()
		
	def save(self):
		db.session.commit()

class Blog(db.Model):
	id = db.Column(db.Integer, primary_key=True, nullable=False)
	user = db.relationship("User",
		backref=db.backref('blogs', lazy=True))
		
	title = db.Column(db.String(30), nullable=False)
	content = db.Column(db.Text, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
	date_created = db.Column(db.DateTime, nullable=False)
	
	def create(self):
		db.session.add(self)
		db.session.commit()
		
	def delete(self):
		db.session.delete(self)
		db.session.commit()
		
	def save(self):
		db.session.commit()

