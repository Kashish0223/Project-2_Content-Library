from flask import Flask, render_template, request, redirect, send_from_directory, url_for, session, flash
from extension import database
from model import User, Course, Document, Module, Video
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Connect the Flask app (server) with SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Add this line

# Create object of SQLAlchemy
database.init_app(app)
migrate = Migrate(app, database)

# Set the directory where the static files are stored
UPLOAD_FOLDER = 'static/images'
UPLOAD_VIDEO = 'static/videos'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_VIDEO'] = UPLOAD_VIDEO

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'mp4'}

# Set the directory where the static documents are stored
UPLOAD_DOCUMENT = 'static/documents'
app.config['UPLOAD_DOCUMENT'] = UPLOAD_DOCUMENT
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'xlsx', 'xls', 'ppt'}

# Creating the routes
@app.route('/index')
def index():
    if 'role' not in session or session['role'] != 'teacher':
        flash('You do not have access to this page.', 'danger')
        return redirect('/login')
    return render_template("index.html")

@app.route('/')
def home():
    if 'role' not in session or session['role'] != 'student':
        flash('You do not have access to this page.', 'danger')
        return redirect('/login')
    return render_template("home.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['username'] = user.username
            session['role'] = user.role
            flash('Login successful!', 'success')
            if user.role == 'student':
                return redirect('/')
            elif user.role == 'teacher':
                return redirect('/index')
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        if not username or not email or not password or not role:
            flash('All fields are required!', 'danger')
            return redirect('/register')
        
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, email=email, password=hashed_password, role=role)
        database.session.add(new_user)
        database.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect('/login')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    flash('You have been logged out.', 'info')
    return redirect('/login')

@app.route('/contact')
def contact():
    if 'role' not in session or session['role'] != 'student':
        flash('You do not have access to this page.', 'danger')
        return redirect('/login')
    return render_template("contact.html")

@app.route('/about')
def about():
    if 'role' not in session or session['role'] != 'student':
        flash('You do not have access to this page.', 'danger')
        return redirect('/login')
    return render_template("about.html")

##############---------Module Route start---------################
@app.route('/add_module', methods=['GET', 'POST'])
def add_module():
    if 'role' not in session or session['role'] != 'teacher':
        flash('You do not have access to this page.', 'danger')
        return redirect('/login')
    
    if request.method == "POST":
        modtitle = request.form.get('title')
        moddescription = request.form.get('description')
        mcourse = request.form.get('course')
        moddate_str = request.form.get('mod_date')
       
        try:
            mod_date = datetime.strptime(moddate_str, '%Y-%m-%d').date()
        except ValueError:
            return "Invalid date format. Please use YYYY-MM-DD."

        modadd = Module(title=modtitle, description=moddescription, course_id=mcourse, mod_date=mod_date)
        database.session.add(modadd)
        database.session.commit()

        # Returning the response
        return redirect("/add_module")
    else:
        # Fetch all the modules from the database
        allModule = Module.query.all()
        courses = Course.query.with_entities(Course.id, Course.ctitle).all()

        # Returning the response
        return render_template("add_module.html", allModule=allModule, courses=courses)

@app.route('/moddelete')
def moddelete():
    if 'role' not in session or session['role'] != 'teacher':
        flash('You do not have access to this page.', 'danger')
        return redirect('/login')
    # extract the id
    serial_number = request.args.get('id')

    # extract the id
    mod_id = Module.query.filter_by(id=serial_number).first()

    database.session.delete(mod_id)
    database.session.commit()

    return redirect("/add_module")

@app.route('/modupdate', methods=["GET", "POST"])
def modupdate(): 
    if 'role' not in session or session['role'] != 'teacher':
        flash('You do not have access to this page.', 'danger')
        return redirect('/login')
    
    # getting serial number from the module
    serial_number = request.args.get('id')
    reqmod = Module.query.filter_by(id=serial_number).first()
    
    if request.method == 'POST':
        # Update the title 
        updatedtitle = request.form.get('title')
        updateddescription = request.form.get('description')
        updatedcourse_id = request.form.get('course')
        updateddate = request.form.get('mod_date')

        # Validate and convert the date
        try:
            updateddate = datetime.strptime(updateddate, '%Y-%m-%d')
        except ValueError:
            flash('Invalid date format. Please use YYYY-MM-DD.', 'danger')
            return redirect(request.url)
        
        # changing the value of existing module
        reqmod.title = updatedtitle
        reqmod.description = updateddescription
        reqmod.course_id = updatedcourse_id  # Assuming course_id is the foreign key field
        reqmod.mod_date = updateddate

        # committing changes to database
        database.session.add(reqmod)
        database.session.commit()
        
        return redirect("/add_module")
    else:
        courses = Course.query.all()
        return render_template("modupdate.html", courses=courses, reqmod=reqmod)

##############---------Module Route End---------################

##############---------Course Route start---------################
@app.route('/add_course',methods=['GET','POST'])
def add_course():
    if 'role' not in session or session['role'] != 'teacher':
        flash('You do not have access to this page.', 'danger')
        return redirect('/login')
    if request.method == "POST":
        
        cattitle = request.form.get('ctitle')
        catdescription = request.form.get('cdescription')
        catdate_str = request.form.get('cdate')
       
        try:
            catdate = datetime.strptime(catdate_str, '%Y-%m-%d').date()
        except ValueError:
            return "Invalid date format. Please use YYYY-MM-DD."

        catadd = Course(ctitle=cattitle, cdescription=catdescription, cdate=catdate)
        database.session.add(catadd)
        database.session.commit()
        # returning the response
        return redirect("/add_course")
    else:
        # fetch all the tasks from the database
        allCourse = Course.query.all()

        # returning the response
        return render_template("add_course.html", allCourse=allCourse)

@app.route('/catdelete')
def delete():
    if 'role' not in session or session['role'] != 'teacher':
        flash('You do not have access to this page.', 'danger')
        return redirect('/login')
    # extract the id
    serial_number = request.args.get('id')

    # extract the id
    cat_id = Course.query.filter_by(id=serial_number).first()

    database.session.delete(cat_id)
    database.session.commit()

    return redirect("/add_course")

@app.route('/coupdate', methods=["GET", "POST"])
def coupdate(): 
    if 'role' not in session or session['role'] != 'teacher':
        flash('You do not have access to this page.', 'danger')
        return redirect('/login')
    
    # getting serial number from the database
    serial_number = request.args.get('id')
    reqcat = Course.query.filter_by(id=serial_number).first()
    
    if request.method == 'POST':
        # Update the title 
        updatedtitle = request.form.get('ctitle')
        updateddescription = request.form.get('cdescription')
        updateddate = request.form.get('cdate')

        # Validate and convert the date
        try:
            updateddate = datetime.strptime(updateddate, '%Y-%m-%d')
        except ValueError:
            flash('Invalid date format. Please use YYYY-MM-DD.', 'danger')
            return redirect(request.url)
        
        # changing the value of existing task
        reqcat.ctitle = updatedtitle
        reqcat.cdescription = updateddescription
        reqcat.cdate = updateddate

        # committing changes to database
        database.session.add(reqcat)
        database.session.commit()
        
        return redirect("/add_course")
    else:
        return render_template("coupdate.html", reqcat=reqcat)

##############---------Course Route End---------################

if __name__ == "__main__":
    app.run(debug=True)
