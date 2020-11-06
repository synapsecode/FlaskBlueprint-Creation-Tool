import os
import sys
import subprocess

class FlaskBluePrintCreationTool:
	directory = ''
	name_identifier = ''
	packages = ['flask', 'flask-sqlalchemy', 'flask_cors', 'Flask-Caching']

	def file_writer(self, name, source):
		with open(os.path.join(self.directory, self.name_identifier, name), "w") as f:
			f.write(source)
		print("Created: " + os.path.join(self.directory, self.name_identifier, name))

	def __init__(self, directory):
		self.directory = directory

	def create_env(self):
		print("Creating Virtual Environment (will take some time)...")
		proc = subprocess.Popen('virtualenv venv', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
		out, err = proc.communicate()
		print("Created: Python Virtual Environment (venv)")
		
	#pip install major dependencies
	def install_dependencies(self):
		print("Installing Packages (will take some time...)")
		command = f'"venv/Scripts/activate" && pip install {" ".join(self.packages)}'
		proc = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
		out, err = proc.communicate()
		print("Installed: Flask Packages & Dependencies")
		print(f"Installed: [{', '.join(self.packages)}]")

	def create_project(self, name):
		self.name_identifier = name
		#Make Root folder
		os.mkdir(f"{self.directory}/{self.name_identifier}/")
		os.chdir(os.path.join(self.directory, self.name_identifier))
		print("Created: Root")

		self.create_env() #Create Virual Environment

		#Root file declarations
		self.file_writer("readme.txt", \
f"""This is the way a basic {self.name_identifier} App is Structured
run.py is the runner of your App
This app comes with its own Python 3.7 virtual environment

{self.name_identifier} /
	__init__.py handles the creation of the app, blueprint registration and more
	config.py has some variables that can alter the way the app works
	models.py contains your FlaskSQLAlchemy database models
	/static - static assets
	/templates - Jinja Templates
	/main - This is your first blueprint module
		__init__.py tells python that this is a python module
		routes.py actually has all the routes served under that blueprint! You write most of your code there.
	
	As you create new blueprint modules, import them and add them to __init__.py in the project root.
	To Create database:
		-> Open Terminal
		-> activate virtual environment
		-> run "from {self.name_identifier} import create_database
				create_database()"
		-> Your database has been created!

To run the app:
	-> activate virtual environment
	-> python run.py
""") #Readme.txt file



		self.file_writer("run.py", \
f"""from {self.name_identifier} import create_app
from {self.name_identifier}.config import Config

app = create_app()
config = Config()
if __name__ == '__main__':
	#Runs on localhost:8080
	app.run(debug=config.PRODUCTION_MODE, host=config.HOST_NAME, port=config.PORT_NUMBER)
""") #Run.py

		self.file_writer("start.bat", \
f"""@echo off
"venv/Scripts/activate" && python run.py
pause
""")




		#Make Subroot folder
		subroot = os.path.join(self.directory, self.name_identifier, self.name_identifier)
		os.mkdir(subroot)
		os.chdir(os.path.join(subroot))
		print("Created: SubRoot")

		#Making Folders
		os.mkdir(os.path.join(subroot, 'static'))
		os.mkdir(os.path.join(subroot, 'templates'))


		#Making Necessary Files
		self.file_writer(f"{self.name_identifier}/__init__.py", \
f"""from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from {self.name_identifier}.config import Config
from flask_cors import CORS

db = SQLAlchemy()

def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)
	db.init_app(app)
	CORS(app)

	#Import all your blueprints
	from {self.name_identifier}.main.routes import main
	
	#use the url_prefix arguement if you need prefixes for the routes in the blueprint
	app.register_blueprint(main)

	return app

#Helper function to create database file directly from terminal
def create_database():
	import {self.name_identifier}.models
	print("Creating App & Database")
	app = create_app()
	with app.app_context():
		db.create_all()
		db.session.commit()
	print("Successfully Created Database")
""") #subroot level __init__.py

		self.file_writer(f"{self.name_identifier}/config.py", \
f"""import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY = "2F5F6CE5AE30B54AA5D7CED1BA566982BAB34BA2814A51CE1865D2C2D8815CD4"
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite') #Database path
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	PRODUCTION_MODE = False #This states whether the app runs in DEBUG MODE or not
	PORT_NUMBER = 8080
	HOST_NAME = 'localhost'
""") #subroot level config.py

		self.file_writer(f"{self.name_identifier}/models.py", \
f"""#Database Layer
from datetime import datetime
from flask import current_app
from {self.name_identifier} import db

class TestModel(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	test_name = db.Column(db.String)
""") #subroot level modles.py

		#populate HTML File
		os.chdir(os.path.join(subroot, 'templates'))
		self.file_writer(f"{os.path.join(subroot, 'templates')}/index.html", \
f"""<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>{self.name_identifier}</title>
</head>
<body>
	
</body>
</html>
""") #subroot level templates/index.html
		os.chdir(subroot)

		#Create the main blueprint
		mbdir = os.path.join(subroot, 'main')
		os.mkdir(mbdir)
		os.chdir(mbdir)

		self.file_writer(f"{mbdir}/__init__.py", \
f"""
""") #subroot level config.py

		self.file_writer(f"{mbdir}/routes.py", \
f"""from flask import render_template, request, Blueprint
main = Blueprint('main', __name__)

@main.route("/")
def main_home():
	return "This is the main module of {self.name_identifier}"
""") #subroot level modles.py
		os.chdir(subroot)

		os.chdir(os.path.join(self.directory, self.name_identifier))
		self.install_dependencies()

		#ending redirect
		os.chdir(self.directory)


	def create_blueprint(self, name):

		x = name.split("/")
		subroot = os.path.join(self.directory, x[0], x[0])
		os.chdir(subroot)

		blueroot = os.path.join(subroot, x[1])
		os.mkdir(blueroot)

		self.file_writer(f"{blueroot}/__init__.py", \
f"""
""") #blueroot level __init__.py

		self.file_writer(f"{blueroot}/routes.py", \
f"""from flask import render_template, request, Blueprint
{x[1]} = Blueprint('{x[1]}', __name__)

@{x[1]}.route("/")
def {x[1]}_home():
	return "This is the {x[1]} module of {x[0]}"
""") #blueroot level routes.py

		dat = ""
		with open(os.path.join(subroot, '__init__.py'), "r") as f:
			dat = f.read()
			#Updating Imports
			dat = dat.replace(f"from {x[0]}.main.routes import main", f"from {x[0]}.main.routes import main\n	from {x[0]}.{x[1]}.routes import {x[1]}")
			#Updating registration
			dat = dat.replace(f"app.register_blueprint(main)", f"app.register_blueprint(main)\n	app.register_blueprint({x[1]}, url_prefix='/{x[1]}')")

		#Writing to the file
		with open(os.path.join(subroot, '__init__.py'), "w") as f:
			f.write(dat)

		print("Updated: __init__.py")

	def delete_blueprint(self, name):
		x = name.split("/")
		import shutil
		loc = os.path.join(self.directory, x[0], x[0], x[1])
		shutil.rmtree(loc)
		print(f"Deleted: Blueprint '{x[1]}' from Flask Project '{x[0]}'")

	def delete_project(self, name):
		import shutil
		shutil.rmtree(os.path.join(self.directory, name))
		print(f"Deleted: Flask Project '{name}''")


if(__name__ == '__main__'):
	print("===== Flask Blueprint Creation Tool =====")
	#CMD Args
	directory = sys.argv[1]
	command = sys.argv[2]
	subcommand = sys.argv[3]
	identifier = sys.argv[4]

	fbct = FlaskBluePrintCreationTool(directory)
	if(command == "create"):
		if(subcommand == "project"):
			fbct.create_project(identifier)
		elif(subcommand == "blueprint"):
			fbct.create_blueprint(identifier)
	elif(command == "delete"):
		if(subcommand == "project"):
			fbct.delete_project(identifier)
		elif(subcommand == "blueprint"):
			fbct.delete_blueprint(identifier)
	print("=============== DONE ====================")
