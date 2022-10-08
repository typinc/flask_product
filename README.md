## General information  
Simple Flask static website for product display.  
Responsive layout.  
Very lightweight.
# DEVELOPMENT     
index.html is different from other pages of the site. Add code in index.html if you add in base.html

## How to use  
1. Install python 3 including pip
2. Install tox
3. Clone repository
4. Create a venv if needed
5. Run pip install -r requirements.txt
6. Create a database in the "/database" folder with sqlite3 databse.db
   1. Than use "python3 -m 'from app import db; db.create_all();"
   2. Optional : if the database already exists, delete it and let the flaskapp.py create it
7. Run python app.py  

# PRODUCTION

  

