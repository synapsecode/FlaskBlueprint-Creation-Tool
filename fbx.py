import os
import sys
import subprocess
import shutil
import glob

#TODO: Exception Handling Using Function Decorators
#TODO: add encoding=utf8 to ALl file opens
#TODO: Output better stuff
#TODO: Add Text Colouring???

#! Random Encoding Errors Occuring Sparsely

class FlaskBlueprintCreator:
	directory = ''
	project_name = ''

	def __init__(self, directory, project_name):
		self.directory = directory
		project_name = project_name if (len(project_name.split("/")) == 1) else project_name.split("/")[0]
		self.project_name = project_name

	#This Function Writes files to the respective directories and logs the status out
	def file_writer(self, filename, source):
		with open(os.path.join(self.directory, self.project_name, filename), "w") as f:
			f.write(source)
		print("Created: " + os.path.join(self.directory, self.project_name, filename))

	def get_blueprint_route(self, project_name, name):
		return f"""from flask import render_template, request, Blueprint
{name} = Blueprint('{name}', __name__)

@{name}.route("/")
def {name}_home():
	return "This is the {name} module of {project_name}"
"""

	#This Function uses Virtualenv to create a new Virtual Environment in the Root Directory
	def create_virtual_env(self):
		print("Creating Virtual Environment (might take some time)...")
		proc = subprocess.Popen('virtualenv venv', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
		out, err = proc.communicate()
		print("Created: Python Virtual Environment (venv)")

	def hard_delete_tree(self, dx):
		import stat

		def on_rm_error(func, path, exc_info):
			os.chmod(path, stat.S_IWRITE)
			os.unlink(path)
		
		for i in os.listdir(dx):
			if i.endswith('git'):
				tmp = os.path.join(dx, i)
				while True:
					subprocess.call(['attrib', '-H', tmp])
					break
				shutil.rmtree(tmp, onerror=on_rm_error)
		shutil.rmtree(dx)


	def git_clone(self):
		print("Cloning Base Project (might take some time)...")
		proc = subprocess.Popen('git clone https://github.com/synapsecode/Flask-APIBlueprintTemplate.git', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
		out, err = proc.communicate()
		print("Cloned: BaseProject")

		src = os.path.join(self.directory, 'Flask-APIBlueprintTemplate', 'ExampleAPI')
		dst = os.path.join(self.directory)
		shutil.move(src, dst)
		
		self.hard_delete_tree(os.path.join(self.directory,'Flask-APIBlueprintTemplate'))
		print("\nCleaned Up Successfully")

	def replace_in_files(self, before, after, ext):
		for filepath in glob.iglob(f'./**/*.{ext}', recursive=True):
			with open(filepath, encoding="utf8") as file:
				s = file.read()
			s = s.replace(before, after)
			with open(filepath, "w", encoding='utf8') as file:
				file.write(s)

	def manipulate_files(self):
		os.rename(os.path.join(self.directory,'ExampleAPI'), os.path.join(self.directory,self.project_name))
		os.rename(os.path.join(self.directory, self.project_name, 'ExampleAPI'), os.path.join(self.directory, self.project_name, self.project_name))

		#Delete __pycache__ files
		xd = os.path.join(self.directory, self.project_name, self.project_name)
		shutil.rmtree(os.path.join(xd, '__pycache__'))
		shutil.rmtree(os.path.join(xd, 'main', '__pycache__'))

		#Traverse Tree for each file, and replace 'ExampleAPI' with Project Name
		self.replace_in_files("ExampleAPI", self.project_name, 'py')
		self.replace_in_files("ExampleAPI", self.project_name, 'txt')

		#Returns New Root
		return os.path.join(self.directory,self.project_name)

	def install_dependencies(self):
		print("Installing PIP Packages (might take some time)...")
		proc = subprocess.Popen('"venv/Scripts/activate" && pip install -r requirements.txt', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
		out, err = proc.communicate()
		print("Installed: Python Dependencies")
		os.remove(os.path.join(self.directory, self.project_name, 'requirements.txt'))

	
	#==================================RUNNERS=================================================

	def create_api(self):
		os.chdir(os.path.join(self.directory)) #Move into Destination Directory
		self.git_clone() #Perform a GitClone (in dest)
		n_root = self.manipulate_files() #Manipulate the Cloned Folder Structure
		os.chdir(n_root) #Move to new Root
		self.create_virtual_env()
		self.install_dependencies()

	#Deletion
	def delete_rest_api(self):
		print("Deleting Flask(Blueprint) REST_API")
		import shutil
		shutil.rmtree(os.path.join(self.directory, self.project_name))
		print(f"Deleted: Flask Project '{self.project_name}''")

	def create_rest_blueprint(self, name):
		subroot = os.path.join(self.directory, self.project_name, self.project_name)
		os.chdir(subroot) #Enter Subroot
		blueroot = os.path.join(subroot, name)
		os.mkdir(blueroot) #Create Blueprint Directory

		#Writing to new Files inside Blueprint
		self.file_writer(f"{blueroot}/__init__.py", "")
		self.file_writer(f"{blueroot}/routes.py", self.get_blueprint_route(self.project_name, name))

		#Modifying subroot __init__.py file
		dat = ""
		with open(os.path.join(subroot, '__init__.py'), "r") as f:
			dat = f.read()
			#Updating Imports
			dat = dat.replace(f"from {self.project_name}.main.routes import main", f"from {self.project_name}.main.routes import main\n	from {self.project_name}.{name}.routes import {name}")
			#Updating registration
			dat = dat.replace(f"app.register_blueprint(main)", f"app.register_blueprint(main)\n	app.register_blueprint({name}, url_prefix='/{name}')")

		#Writing to the file (subroot __init__.py)
		with open(os.path.join(subroot, '__init__.py'), "w") as f:
			f.write(dat)

		print("Updated: __init__.py")
		print(f"Successfully Created REST_API Blueprint: '{name}'")


	def delete_blueprint(self, name):
		import shutil
		loc = os.path.join(self.directory, self.project_name, self.project_name, name)
		shutil.rmtree(loc)
		print(f"Deleted: Blueprint '{name}' from Flask Project '{self.project_name}'")


if(__name__ == '__main__'):
	print("========== Flask Blueprint Creation Tool ==========")
	directory = sys.argv[1]
	c1 = sys.argv[2]
	c2 = sys.argv[3]
	c3 = sys.argv[4]

	fbc = FlaskBlueprintCreator(directory=directory, project_name=c3)

	if(c1 == 'create'):
		if(c2 == 'api'):
			fbc.create_api()
		elif(c2 == 'project'):
			pass
		elif(c2 == 'blueprint'):
			fbc.create_rest_blueprint(c3.split("/")[1])
		elif(c2 == 'project-blueprint'):
			pass
	elif(c1 == 'delete'):
		if(c2 == 'api'):
			fbc.delete_rest_api()
		elif(c2 == 'project'):
			pass
		elif(c2 == 'blueprint'):
			fbc.delete_blueprint(c3.split("/")[1])
	print("==================== DONE ========================")