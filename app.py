from multiprocessing.managers import Server
from flask import Flask, render_template, request, redirect, send_from_directory, url_for, session, flash
from extension import database
from model import User, Course, Document, Module, Video
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_migrate import Migrate
import os
from waitress import serve

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your_default_secret_key')

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///library.db')
# postgresql://library_sql_user:SVhrlpx5HWu17QBUvJAucjTmZgha78ZP@dpg-cqlrv3ggph6c738lman0-a.oregon-postgres.render.com/library_sql
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
database.init_app(app)
migrate = Migrate(app, database)

UPLOAD_FOLDER = 'static/images'
UPLOAD_VIDEO = 'static/videos'
UPLOAD_DOCUMENT = 'static/documents'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_VIDEO'] = UPLOAD_VIDEO
app.config['UPLOAD_DOCUMENT'] = UPLOAD_DOCUMENT
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'mp4', 'pdf', 'doc', 'docx', 'xlsx', 'xls', 'ppt'}

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
if not os.path.exists(app.config['UPLOAD_VIDEO']):
    os.makedirs(app.config['UPLOAD_VIDEO'])
if not os.path.exists(app.config['UPLOAD_DOCUMENT']):
    os.makedirs(app.config['UPLOAD_DOCUMENT'])

if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    handler = RotatingFileHandler('error.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.ERROR)
    app.logger.addHandler(handler)

with app.app_context():
    database.create_all()

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
            flash('Invalid date format. Please use YYYY-MM-DD.', 'danger')
            return redirect(request.url)

        modadd = Module(title=modtitle, description=moddescription, course_id=mcourse, mod_date=mod_date)
        database.session.add(modadd)
        database.session.commit()

        flash('Module added successfully!', 'success')
        return redirect("/add_module")
    else:
        allModule = Module.query.all()
        courses = Course.query.with_entities(Course.id, Course.ctitle).all()
        return render_template("add_module.html", allModule=allModule, courses=courses)

@app.route('/moddelete')
def moddelete():
    if 'role' not in session or session['role'] != 'teacher':
        flash('You do not have access to this page.', 'danger')
        return redirect('/login')
    serial_number = request.args.get('id')
    mod_id = Module.query.filter_by(id=serial_number).first()
    database.session.delete(mod_id)
    database.session.commit()
    return redirect("/add_module")

@app.route('/modupdate', methods=["GET", "POST"])
def modupdate():
    if 'role' not in session or session['role'] != 'teacher':
        flash('You do not have access to this page.', 'danger')
        return redirect('/login')
    
    serial_number = request.args.get('id')
    reqmod = Module.query.filter_by(id=serial_number).first()
    
    if request.method == 'POST':
        updatedtitle = request.form.get('title')
        updateddescription = request.form.get('description')
        updatedcourse_id = request.form.get('course')
        updateddate = request.form.get('mod_date')

        try:
            updateddate = datetime.strptime(updateddate, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format. Please use YYYY-MM-DD.', 'danger')
            return redirect(request.url)
        
        reqmod.title = updatedtitle
        reqmod.description = updateddescription
        reqmod.course_id = updatedcourse_id
        reqmod.mod_date = updateddate

        database.session.add(reqmod)
        database.session.commit()
        
        flash('Module updated successfully!', 'success')
        return redirect("/add_module")
    else:
        courses = Course.query.all()
        return render_template("modupdate.html", courses=courses, reqmod=reqmod)

@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    if 'role' not in session or session['role'] != 'teacher':
        flash('You do not have access to this page.', 'danger')
        return redirect('/login')
    
    if request.method == "POST":
        ctitle = request.form.get('title')
        cdescription = request.form.get('description')
        cdate_str = request.form.get('c_date')
        
        try:
            c_date = datetime.strptime(cdate_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format. Please use YYYY-MM-DD.', 'danger')
            return redirect(request.url)

        course = Course(ctitle=ctitle, cdescription=cdescription, c_date=c_date)
        database.session.add(course)
        database.session.commit()

        flash('Course added successfully!', 'success')
        return redirect("/add_course")
    else:
        allCourse = Course.query.all()
        return render_template("add_course.html", allCourse=allCourse)

@app.route('/coursedelete')
def coursedelete():
    if 'role' not in session or session['role'] != 'teacher':
        flash('You do not have access to this page.', 'danger')
        return redirect('/login')
    serial_number = request.args.get('id')
    cour_id = Course.query.filter_by(id=serial_number).first()
    database.session.delete(cour_id)
    database.session.commit()
    return redirect("/add_course")

@app.route('/courseupdate', methods=["GET", "POST"])
def courseupdate():
    if 'role' not in session or session['role'] != 'teacher':
        flash('You do not have access to this page.', 'danger')
        return redirect('/login')
    
    serial_number = request.args.get('id')
    reqcourse = Course.query.filter_by(id=serial_number).first()
    
    if request.method == 'POST':
        updatedtitle = request.form.get('title')
        updateddescription = request.form.get('description')
        updateddate = request.form.get('c_date')

        try:
            updateddate = datetime.strptime(updateddate, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format. Please use YYYY-MM-DD.', 'danger')
            return redirect(request.url)
        
        reqcourse.ctitle = updatedtitle
        reqcourse.cdescription = updateddescription
        reqcourse.c_date = updateddate

        database.session.add(reqcourse)
        database.session.commit()
        
        flash('Course updated successfully!', 'success')
        return redirect("/add_course")
    else:
        return render_template("courseupdate.html", reqcourse=reqcourse)

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@app.route('/upload_image', methods=['GET', 'POST'])
def upload_image():
    if 'role' not in session or session['role'] != 'teacher':
        flash('You do not have access to this page.', 'danger')
        return redirect('/login')

    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename, {'jpg', 'jpeg', 'png'}):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_image', filename=filename))
        else:
            flash('Invalid file type.', 'danger')
            return redirect(request.url)
    return render_template('upload_image.html')

@app.route('/uploaded_image/<filename>')
def uploaded_image(filename):
    return render_template('uploaded_image.html', filename=filename)

@app.route('/upload_video', methods=['GET', 'POST'])
def upload_video():
    if 'role' not in session or session['role'] != 'teacher':
        flash('You do not have access to this page.', 'danger')
        return redirect('/login')
    
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename, {'mp4'}):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_VIDEO'], filename))
            return redirect(url_for('uploaded_video', filename=filename))
        else:
            flash('Invalid file type.', 'danger')
            return redirect(request.url)
    return render_template('upload_video.html')

@app.route('/uploaded_video/<filename>')
def uploaded_video(filename):
    return render_template('uploaded_video.html', filename=filename)

@app.route('/upload_document', methods=['GET', 'POST'])
def upload_document():
    if 'role' not in session or session['role'] != 'teacher':
        flash('You do not have access to this page.', 'danger')
        return redirect('/login')
    
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename, {'pdf', 'doc', 'docx', 'xlsx', 'xls', 'ppt'}):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_DOCUMENT'], filename))
            return redirect(url_for('uploaded_document', filename=filename))
        else:
            flash('Invalid file type.', 'danger')
            return redirect(request.url)
    return render_template('upload_document.html')

@app.route('/uploaded_document/<filename>')
def uploaded_document(filename):
    return render_template('uploaded_document.html', filename=filename)

# @app.route('/download_document/<int:document_id>')
# def download_document(document_id):
#     doc = Document.query.get_or_404(document_id)
#     return send_from_directory(app.config['UPLOAD_DOCUMENT'], os.path.basename(doc.document_path))

##############---------Content Library Route Start---------################
@app.route('/ContentLibrary')
def content_library():
    if 'role' not in session or session['role'] != 'student':
        flash('You do not have access to this page.', 'danger')
        return redirect('/login')
    allmodule = Module.query.all()
    all_video = Video.query.all()
    documents = Document.query.all()
    allcourse = Course.query.with_entities(Course.id, Course.ctitle).all()
    print(all_video)
    return render_template('ContentLibrary.html',allmodule=allmodule,all_video=all_video,
                           documents=documents, 
                           allcourse=allcourse)

@app.route('/add_content', methods=['GET', 'POST'])
def add_content():
    if 'role' not in session or session['role'] != 'teacher':
        flash('You do not have access to this page.', 'danger')
        return redirect('/login')
    
    if request.method == 'POST':
        # Handle form submission
        title = request.form.get('title')
        description = request.form.get('description')
        course_id = request.form.get('course')
        image = request.files.get('img')
        document = request.files.get('docu')
        ddate_str = request.form.get('docdate')
       
        # Convert the string to a date object
        try:
            docdate = datetime.strptime(ddate_str, '%Y-%m-%d').date()
        except ValueError:
            return "Invalid date format. Please use YYYY-MM-DD."

        # Save the image file
        if image:
            image_filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename).replace('\\', '/')
            image.save(image_path)
        else:
            image_path = None
        
        # Save the document file
        if document:
            document_filename = secure_filename(document.filename)
            document_path = os.path.join(app.config['UPLOAD_DOCUMENT'], document_filename).replace('\\', '/')
            document.save(document_path)
        else:
            document_path = None

        # Create a new content item
        new_content = Document(
            title=title,
            description=description,
            image_path=image_path,
            document_path=document_path,
            course_id=course_id,
            docdate=docdate
        )
        database.session.add(new_content)
        database.session.commit()

        flash('Content added successfully!', 'success')
        return redirect('/add_content')
    else:
        # Fetch the courses and render the template
        allmodule = Module.query.with_entities(Module.id, Module.title).all()
        documents = Document.query.all()
        all_video = Video.query.all()
        allcourse = Course.query.all()
        return render_template('add_content.html', allmodule=allmodule, allcourse=allcourse, documents=documents, all_video=all_video)
@app.route('/contentdelete')
def contentdelete():
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
        reqcontent.title = request.form['title']
        reqcontent.description = request.form['description']
        reqcontent.course_id = request.form['course']
        # reqcontent.docdate = request.form['docdate']
        
        ddate_str = request.form['docdate']
        try:
            reqcontent.docdate = datetime.strptime(ddate_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format. Please use YYYY-MM-DD.', 'danger')
            return redirect('/contentupdate?id=' + content_id)

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
    doc = Document.query.get_or_404(document_id)
    # Logic to serve/download the document file
    return send_from_directory(app.config['UPLOAD_FOLDER'],  os.path.basename(doc.document_path))
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

##############---------Content Library Route End---------################

##############---------Video Route Start---------################
@app.route('/add_videos', methods=['GET', 'POST'])
def add_videos():
    if 'role' not in session or session['role'] != 'teacher':
        flash('You do not have access to this page.', 'danger')
        return redirect('/login')

    if request.method == 'POST':
        video_title = request.form.get('video_title')
        video_id = request.form.get('video_id')
        vdate_str = request.form.get('video_date')

        # Convert the string to a date object
        try:
            video_date = datetime.strptime(vdate_str, '%Y-%m-%d').date()
        except ValueError:
            return "Invalid date format. Please use YYYY-MM-DD."

        thumbnail_path = f"https://img.youtube.com/vi/{video_id}/0.jpg"

        # Create a new video item
        new_video = Video(
            video_title=video_title,
            video_id=video_id,
            video_date=video_date,
            thumbnail_path=thumbnail_path
        )
        database.session.add(new_video)
        database.session.commit()

        flash('Video added successfully!', 'success')
        return redirect('/add_videos')
    else:
        # Fetch the videos and render the template
        all_video = Video.query.all()
        return render_template('add_videos.html', all_video=all_video)
@app.route('/embed_video', methods=['POST', 'GET'])
def embed_video():
    if request.method == 'POST':
        video_id = request.form['video_id']
        return render_template('ContentLibrary.html', video_id=video_id)

    return render_template('ContentLibrary.html')

@app.route('/videoupdate/<int:video_id>', methods=["GET", "POST"])
def videoupdate(video_id):
    video = Video.query.get_or_404(video_id)

    if request.method == 'POST':
        video.video_title = request.form['video_title']
        video.video_id = request.form['video_id']
        videodate_str = request.form.get('video_date')

        video.video_date = datetime.strptime(videodate_str, '%Y-%m-%d').date()
        
        database.session.commit()
        flash('Video updated successfully', 'success')
        return redirect(url_for('add_videos'))  
    
    return render_template('videoupdate.html', video=video)


@app.route('/videodelete', methods=['GET','POST'])
def videodelete():
    video_id = request.form.get('id')

    video = Video.query.get_or_404(video_id)

    database.session.delete(video)
    database.session.commit()

    return redirect(url_for('add_videos'))


if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=8000)
