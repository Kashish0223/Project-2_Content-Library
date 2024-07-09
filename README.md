# Content Library Project

## Table of Contents
- [Project Description](#project-description)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Contributing](#contributing)
- [Contact](#contact)

## Project Description
The Content Library Project is a web application designed for managing educational content. The application features two types of users: Admin (or Teacher) and Student. The Admin/Teacher can add, update, and delete courses, as well as manage the content media library. Students can view available courses and access the content media library.

## Features
- **User Authentication:** Separate login and registration for Admin/Teacher and Students.
- **Student Pages:**
  - Login/Register
  - Index
  - About Us
  - Contact Us
  - Products
  - Content Media Library
- **Admin/Teacher Pages:**
  - Login/Register
  - Add Courses
  - Add Content
  - Add Modules

## Technologies Used
- **Frontend:** HTML, CSS
- **Backend:** Flask
- **Database:** SQLAlchemy


## Project Structure

```plaintext
ContentLibrary/
├── backend/
│   ├── Scripts/                                 # Template of backend file
│   └── ...
├── instance/
│   └── library/                                  # Database file
├── templates/
│   ├── login/                                    # Template of login teacher/student
│   ├── register/                                 # Template of register teacher/student
│   ├── parent/                                   # Template of teacher's index page
│   ├── base/                                     # Template of student's index page
│   ├── product/                                  # Template of product page
│   ├── about_us/                                 # Template of about us page
│   ├── contact_us/                               # Template of contact us page
│   ├── content_media_library/                    # Template of content media library page
│   ├── add_courses/                              # Template of add_courses page
│   ├── add_content/                              # Template of add_content page
│   ├── add_module/                               # Template of add_module page
│   ├── coupdate/                                 # Template of coupdate page
│   ├── contentupdate/                            # Template of contentupdate page
│   ├── modupdate/                                # Template of modupdate page
│
├── static/
│   ├── css/
│   │   ├── login_style/
│   │   ├── base_style/
│   │   └── style/
│   ├── js/
│   │   └── script/
│   ├── images/
│   └── documents/
│
├── app.py
├── database.py
├── extension.py
├── module.py
└── README.md

## Setup Instructions
1. **Folder Path:**
    
    E:\>
    cd SummerProject2


2. **Create a Backend Environment:**

    python -m venv backend


3. **Activate the Environment:**
    
    backend\Scripts\activate


4. **Install Flask and SQLAlchemy:**
    
    pip install flask
    pip install flask_sqlalchemy


5. **Set Up the Database:**
    - Define your database URI in the configuration file.
    - Create the database tables:

          from app import db
          db.create_all()
          exit()


## Usage

1. **Run the Application:**

    python app.py

2. **Access the Application:**                                                                                    - Open your web browser and navigate to http://127.0.0.1:5000/

## Contributing

1. Fork the repository.
2. Create your feature branch: git checkout -b feature/my-new-feature
3. Commit your changes: git commit -am 'Add some feature'
4. Push to the branch: git push origin feature/my-new-feature
5. Submit a pull request.

## Contact

- **Author:** Kashish Sharma   