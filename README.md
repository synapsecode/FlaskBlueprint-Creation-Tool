# FlaskBlueprint Creation Tool
 A simple Python script that generates a Flask blueprint enabled project on demand! and also has the ability to add or remove blueprints.
 
## What are Flask Blueprints?
Flask is a really simple python based microframework for the web. You can create an api with as little as 2 to 3 files and very few lines of code. Flask is perfect for small projects and hobbyist projects. However, flask also has the ability to do much more! You can use it as an API but you can also use it for Server Side Rendering using Jinja2
Hence, for bigger projects, we need a more well defined structure. Enter, Flask Blueprints. This is a flask-prescribed Structure that makes it incredibly simple to create massive apps while still retaining the ease of use that flask is well known for. 

## Why this Script?
Flask Blueprints are a pain to setup. You may often times find yourself cloning templates and then manually editing and renaming everything. My Script does all of that for you. It can also make and delete blueprints on demand. This is incredibly useful if you're serious about development with Flask! It saves enormous amounts of time

## Creating a Flask API Project
A Flask API Project is a simplified version of the Blueprints specification that basically removes all SSR and only enables enough to create REST APIs using Flask. This is very useful if you want to make APIs
> (ALL Calls to be made from outside the project directory)

```
fbx create api <project_name>
```

>>  ### Generated Structure
>>>  Flask Blueprints API Structure
  
  
## Adding Blueprints

```
fbx create blueprint <project_name>/<blueprint_name>
```

>> ### Updated Structure
>>>  Adding a blueprint updates the Folder Tree

## Deleting Blueprints
```
fbx delete blueprint <project_name>/<blueprint_name>
```

## Deleting Flask API Project
```
fbx delete api <project_name>
```


## What does the Script do?
1. Clones a Base Flask Blueprint API Template into the directory from where you call it
2. Modifies it to match your requirements
3. Installs a Python Virtual environment
4. Installs needed dependencies



## Installation (Windows Only)
>> ### 1. Git Clone this project into some folder on your PC
>> ### 2. Make sure you have python3 installed on your PC
>> ### 3. Add the directory path to your environment variables and close cmd and re-open it
>> ### 4. now you can use the "fbx" command in your cmd from any path and it should work!


## Future Roadmap
1. Create Support for Flask Blueprints for Server Side Rendering (SSR)
2. Add support for the --noenv flag to prevent virtual environment creation
3. Keep adding more useful stuff to the base template
