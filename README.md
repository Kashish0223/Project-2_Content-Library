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
## Project Structure

```plaintext
ContentLibrary/
│
├── backend/                 # Backend environment
│   ├── Scripts/             # Activation scripts for the virtual environment
│   └── ...                  # Other files and directories
│
├── instance/                # Instance folder for runtime data
│   └── library/             # Database file
│
├── templates/               # HTML templates
│   ├── register/            # Templates for student/teacher pages
│   ├── login/               # Templates for student/teacher pages
│   ├── parent/              # Templates for parent layout
│   ├── base/                # Templates for base layout
│   ├── product/             # Templates for product pages
│   ├── about_us/            # Templates for "About Us" page
│   ├── contact_us/          # Templates for "Contact Us" page
│   ├── content_media_library/  # Templates for content media library pages
│   ├── add_courses/         # Templates for adding courses
│   ├── add_content/         # Templates for adding content
│   ├── add_module/          # Templates for adding modules
│   ├── coupdate/            # Templates for updating courses
│   ├── contentupdate/         # Templates for updating content
│   ├── modupdate/          # Templates for updating modules
│
├── static/                  # Static files (CSS, JS, images, documents)
│   ├── css/
│   │   ├── login_style/     # CSS for login
│   │   ├── base_style/      # CSS for base layout
│   │   └── style/           # General styles
│   ├── js/
│   │   └── script/          # JavaScript files
│   ├── images/              # Images
│   └── documents/           # Documents
│
├── app.py                   # Main Flask application file
├── database.py              # Database models
├── extension.py             # SQL Extension 
├── model.py                 # All table schema
│
└── README.md                # Project README file
```


## Setup Instructions

1. **Folder Path:**
    ```bash
    E:\>
    cd SummerProject2
    ```

2. **Create a Backend Environment:**
    ```bash
    python -m venv backend
    ```

3. **Activate the Environment:**
    ```bash
    backend\Scripts\activate
    ```

4. **Install Flask and SQLAlchemy:**
    ```bash
    pip install flask
    pip install flask_sqlalchemy
    ```

5. **Set Up the Database:**
    - Define your database URI in the configuration file.
    - Create the database tables:
      ```python
      >>> from app import db
      >>> db.create_all()
      >>> exit()
      ```

## Usage

1. **Run the Application:**
    ```bash
    python app.py
    ```

2. **Access the Application:**
    - Open your web browser and navigate to `http://127.0.0.1:5000/`

## Contributing

1. Fork the repository.
2. Create your feature branch: `git checkout -b feature/my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature/my-new-feature`
5. Submit a pull request.

## Contact

- **Author:** Kashish Sharma
