#!/usr/bin/env python
#

#
import webapp2
import os

import jinja2

from google.appengine.ext import db


template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),autoescape = True)

class Art(db.Model):
	title = db.StringProperty(required=True)
	art = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)





class Handler(webapp2.RequestHandler):

	def write(self,*a,**kw):
		self.response.out.write(*a,**kw)

	def render_str(self,template,**params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self,template,**kw):
		self.write(self.render_str(template,**kw))




class FizzBuzzHandler(Handler):
	def get(self):
		n = self.request.get("n")
		n = int(n)
		self.render("fizzbuzz.html",n = n)


class Rot13Handler(Handler):
	def post(self):
		content = self.request.get("name")

		self.redirect("/?"+urllib.urlencode(content))


class ShoppingHandler(Handler):


	def get(self):

		items = self.request.get_all("food")
		self.render("shopping_list.html",items=items)

class MainHandler(Handler):
	def render_front(self,title ="", art ="",error =""):

		arts = db.GqlQuery("select * from Art order by created desc")
		print arts
		self.render("front.html",title =title,art =art,  error =error,arts=arts)



	def get(self):

		items = self.request.get_all("food")

		self.render("front.html")

	def post(self):

		title = self.request.get("title")
		art = self.request.get("art")

		if  (title and art):
			a = Art(title= title,art=art)
			a.put()
			self.redirect("/")

		else:
			error = "require both title and art"
			self.render_front(title,art,error)






app = webapp2.WSGIApplication([
	('/', MainHandler),('/fizz',FizzBuzzHandler),('/rot13',Rot13Handler),('/shopping',ShoppingHandler)], debug=True)
