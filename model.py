from extension import database


# Create class of table
class User(database.Model):
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    username = database.Column(database.String(50), unique=True, nullable=False)
    email = database.Column(database.String(50), unique=True, nullable=False)
    password = database.Column(database.Text(40), nullable=False)
    role = database.Column(database.String(30), nullable=False, default='student')

class Course(database.Model):
    id = database.Column(database.Integer, primary_key= True, autoincrement=True)
    ctitle = database.Column(database.String(100), nullable= False)
    cdescription = database.Column(database.String(300), nullable= False)
    c_date = database.Column(database.Date, nullable=False)

class Module(database.Model):
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    title = database.Column(database.String(100), nullable=False)
    description = database.Column(database.String(300), nullable=False)
    course_id = database.Column(database.Integer, database.ForeignKey('course.id'), nullable=False)
    course = database.relationship('Course', backref='modules')
    mod_date = database.Column(database.DateTime, nullable=False)

class Document(database.Model):
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    title = database.Column(database.String(100), nullable=False)
    description = database.Column(database.Text, nullable=False)
    image_path = database.Column(database.String(200), nullable=False)
    document_path = database.Column(database.String(200), nullable=False)
    course_id = database.Column(database.Integer, database.ForeignKey('course.id'), nullable=False)
    docdate = database.Column(database.Date,nullable=False)
    course = database.relationship('Course', backref='contents')

class Video(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    video_title = database.Column(database.String(100), nullable=False)
    thumbnail_path = database.Column(database.String(200), nullable=False)
    video_id = database.Column(database.String(100), nullable=False)
    video_date = database.Column(database.DateTime, nullable=False)
