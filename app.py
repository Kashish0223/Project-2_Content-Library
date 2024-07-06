from flask import Flask, render_template, request,redirect, send_from_directory,url_for,session, flash
from extension import database
from model import User, Course, Document,Module
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

#connect the flask app(server) with sqllite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
#create object of SQLAlchemy
database.init_app(app)

# Set the directory where the static files are stored
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

# Set the directory where the static documents are stored
UPLOAD_DOCUMENT = 'static/documents'
app.config['UPLOAD_DOCUMENT'] = UPLOAD_DOCUMENT
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'xlsx', 'xls'}

# Creating the routes
@app.route('/index')
def index():
    if 'role' not in session or session['role'] != 'teacher':
        flash('You do not have access to this page.', 'danger')
        return redirect('/login')
    return render_template("index.html")

@app.route('/')
def base():
    if 'role' not in session or session['role'] != 'student':
        flash('You do not have access to this page.', 'danger')
        return redirect('/login')
    return render_template("base.html")

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

@app.route('/product')
def product():
  if 'role' not in session or session['role'] != 'student':
        flash('You do not have access to this page.', 'danger')
        return redirect('/login')
  return render_template("product.html")

##############---------Module Route start---------################
@app.route('/add_module', methods=['GET', 'POST'])
def add_module():
    if 'role' not in session or session['role'] != 'teacher':
        flash('You do not have access to this page.', 'danger')
        return redirect('/login')
    
    if request.method == "POST":
        # Fetch the values 
        modtitle = request.form.get('title')
        moddescription = request.form.get('description')
        mcourse = request.form.get('course')

        # Add to database
        modadd = Module(title=modtitle, description=moddescription, course_id=mcourse)
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
        
        # changing the value of existing module
        reqmod.title = updatedtitle
        reqmod.description = updateddescription
        reqmod.course_id = updatedcourse_id  # Assuming course_id is the foreign key field
        
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
        
        # fetch the values 
        cattitle = request.form.get('ctitle')
        catdescription = request.form.get('cdescription')
        catdate_str = request.form.get('cdate')
       
           # Convert the string to a date object
        try:
            catdate = datetime.strptime(catdate_str, '%Y-%m-%d').date()
        except ValueError:
            # If the date format is not recognized, return an error
            return "Invalid date format. Please use YYYY-MM-DD."

        # add to database
        catadd = Course(ctitle=cattitle,cdescription=catdescription,cdate=catdate)
        database.session.add(catadd)
        database.session.commit()
         # returning the response
        return redirect("/add_course")
     else:
        # fetch all the tasks from the database
        allCourse = Course.query.all()

        # returning the response
        return render_template("add_course.html",allCourse=allCourse)

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

@app.route('/coupdate',methods=["GET","POST"])
def coupdate(): 
  if 'role' not in session or session['role'] != 'teacher':
        flash('You do not have access to this page.', 'danger')
        return redirect('/login')
    # getting serial no from the course
  serial_number = request.args.get('id')
  reqcat = Course.query.filter_by(id= serial_number).first()
  if request.method == 'POST':
      
      # Update the title 
      updatedtitle = request.form.get('ctitle')
      updateddescription = request.form.get('cdescription')
      updateddate_str = request.form.get('cdate')
        
        # Convert the string to a date object
      try:
            updateddate = datetime.strptime(updateddate_str, '%Y-%m-%d').date()
      except ValueError:
            # If the date format is not recognized, return an error
            return "Invalid date format. Please use YYYY-MM-DD."
      
      # changing the value of existing course
      reqcat.ctitle =  updatedtitle
      reqcat.cdescription = updateddescription
      reqcat.cdate = updateddate

      # committing changes to database
      database.session.add(reqcat)
      database.session.commit()

      return redirect("/add_course")
  else:
      return render_template("coupdate.html",reqcat = reqcat)
##############---------Course Route End---------################

##############---------Product Route start---------################
@app.route('/add_product')
def addproduct():
  if 'role' not in session or session['role'] != 'teacher':
        flash('You do not have access to this page.', 'danger')
        return redirect('/login')
  return render_template("add_product.html")
##############---------Product Route End---------################

##############---------Content Library Route Start---------################
@app.route('/ContentLibrary')
def library():
    if 'role' not in session or session['role'] != 'student':
        flash('You do not have access to this page.', 'danger')
        return redirect('/login')
    documents = Document.query.all()
    return render_template('ContentLibrary.html', documents=documents)

@app.route('/add_content', methods=['GET', 'POST'])
def add_content():
    if 'role' not in session or session['role'] != 'teacher':
        flash('You do not have access to this page.', 'danger')
        return redirect('/login')
    if request.method == 'POST':
        # Handle form submission
        title = request.form['cltitle']
        description = request.form['cldesc']
        course_id = request.form['course']
        image = request.files['img']
        document = request.files['docu']

        # Save the image file
        image_filename = secure_filename(image.filename)
        image_path = os.path.join('static', 'images', image_filename).replace('\\', '/')
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
    
        # Save the document file
        document_filename = secure_filename(document.filename)
        document_path = os.path.join('static', 'documents', document_filename).replace('\\', '/')
        image.save(os.path.join(app.config['UPLOAD_DOCUMENT'], document_filename))

        # Create a new content item
        new_content = Document(title=title, description=description, image_path='images/' + image_filename, document_path='documents/' + document_filename, course_id=course_id)
        database.session.add(new_content)
        database.session.commit()

        return redirect('/add_content')
    else:
        # Fetch the courses and render the template
        courses = Course.query.with_entities(Course.id, Course.ctitle)
        documents = Document.query.all()
        return render_template('add_content.html', courses=courses, documents=documents)

@app.route('/contentdelete')
def contentdelete():
   if 'role' not in session or session['role'] != 'teacher':
        flash('You do not have access to this page.', 'danger')
        return redirect('/login')
   # extract the id
   serial_number = request.args.get('id')

   # extract the id
   con_id = Document.query.filter_by(id=serial_number).first()

   database.session.delete(con_id)
   database.session.commit()

   return redirect("/add_content")

@app.route('/contentupdate', methods=['GET', 'POST'])
def contentupdate():
    content_id = request.args.get('id')
    reqcontent = Document.query.get(content_id)
    if request.method == 'POST':
        reqcontent.title = request.form['ctitle']
        reqcontent.description = request.form['cldesc']
        reqcontent.course_id = request.form['course']
        
        image = request.files['img']
        document = request.files['docu']
        
        if image:
            image_filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename).replace('\\', '/')
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
            reqcontent.image_path = 'images/' + image_filename
        
        if document:
            document_filename = secure_filename(document.filename)
            document_path = os.path.join(app.config['UPLOAD_DOCUMENT'], document_filename).replace('\\', '/')
            document.save(os.path.join(app.config['UPLOAD_DOCUMENT'], document_filename))
            reqcontent.document_path = 'documents/' + document_filename
        
        database.session.commit()
        flash('Content updated successfully!', 'success')
        return redirect('/contentupdate?id=' + content_id)
    
    courses = Course.query.all()
    document = Document.query.all()
    return render_template('contentupdate.html', reqcontent=reqcontent, courses=courses, documents=document)

@app.route('/download_document/<int:document_id>')
def download_document(document_id):
    if 'role' not in session or session['role'] != 'teacher':
        flash('You do not have access to this page.', 'danger')
        return redirect('/login')
    doc = Document.query.get_or_404(document_id)
    # Logic to serve/download the document file
    return send_from_directory(app.config['UPLOAD_FOLDER'],  os.path.basename(doc.document_path))

##############---------Content Library Route End---------################
if __name__ == '__main__':
  # Run the application
  app.run(debug = True)
