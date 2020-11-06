DEPENDENCIES
1. Have virtualenv installed & in path variable

FEATURES
1. Create Project & Blueprint
2. Delete Project & Blueprint

Examples
fbct.py K:/ create project test
fbct.py K:/ delete project test
fbct.py K:/ create blueprint test/auth
fcbt.py K:/ delete blueprint test/auth

STRUCTURE
 HelloFlask
    ├── HelloFlask
    │   ├── __init__.py
    │   ├── config.py
    │   ├── main
    │   │   ├── __init__.py
    │   │   └── routes.py
    │   ├── models.py
    │   ├── static
    │   └── templates
    │       └── index.html
    ├── readme.txt
    ├── run.py
    ├── start.bat
    └── venv