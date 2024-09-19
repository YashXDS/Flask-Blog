# Flask Blog Application

A full-stack blog application built with **Flask**, demonstrating front-end and back-end integration, user authentication, CRUD operations, and file uploads. This project also utilizes **XAMPP** for local MySQL database management and **Apache** server hosting.

## Features

- **User Authentication**: Admin login with session management for secure content management.
- **CRUD Operations**: Create, read, update, and delete blog posts.
- **File Uploads**: Securely upload files and store them on the server.
- **Pagination**: Dynamically load posts with pagination.
- **Contact Form**: Save contact form data to the database.
- **Admin Dashboard**: View and manage posts from a custom dashboard.
  
## Tools & Technologies

### Frontend

- **HTML** for structure and layout.
- **CSS** for styling and responsiveness.
- **Bootstrap** for mobile-first, responsive design.
- **Jinja2** templating for rendering dynamic content.

### Backend

- **Flask**: A Python web framework for routing and application logic.
- **Flask-SQLAlchemy**: ORM for handling MySQL database operations.
- **Flask-Mail**: (Commented out in this version) for sending email notifications.
- **XAMPP**: Used for MySQL database management and Apache server hosting.
  
## Database

The project uses a **MySQL** database for storing:
- **Posts**: Title, slug, tagline, content, and date.
- **Contacts**: Name, email, phone, message, and submission date.

All database operations are handled via **SQLAlchemy**, providing an abstraction layer over raw SQL queries.

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/flask-blog-app.git
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up XAMPP for database:

   Start Apache and MySQL servers from the XAMPP control panel.
   Create a MySQL database and update the config.json file with your database credentials.

4. Modify the config.json file:

   ```json

   {
     "params": {
          "local_uri": "mysql://username:password@localhost/dbname",
          "prod_uri": "mysql://username:password@productionserver/dbname",
          "file_path": "path/to/upload/folder",
          "no_of_posts": 5,
          "admin_name": "admin@example.com",
          "admin_password": "admin_password",
          "gmail-user": "your-email@gmail.com",
          "gmail-password": "your-email-password"
        }
       }
   ```
   
5. Run the application:

  ```bash
     python app.py
  ```

## Access the app at:

```arduino

http://127.0.0.1:5000/

```

## File Structure:

```arduino

├── static
│   ├── css
│   ├── js
├── templates
│   ├── index.html
│   ├── about.html
│   ├── admin.html
│   ├── post.html
│   ├── add.html
│   ├── edit.html
│   ├── login.html
│   ├── contact.html
├── app.py
├── config.json
├── requirements.txt
```

## How It Works

- **Home Page**: Displays blog posts with pagination.
- **Admin Dashboard**: Authenticated users (admin) can add, edit, or delete posts.
- **File Uploads**: Admins can securely upload images or other files.
- **Contact Page**: Submissions from the contact form are saved in the MySQL database.
- **Session Management**: Admin login is maintained via Flask's session handling, allowing secure access to admin-only pages.

### Additional Features

- **Flask-Mail (optional)**: Uncomment the email functionality in app.py to send emails for contact form submissions.
- **Pagination**: Users can navigate through pages of posts dynamically.
- **File Uploads**: Files are securely uploaded and stored using Flask's secure_filename function.

## Future Enhancements
Implement user registration and authentication for non-admin users.
Add rich-text editor support for blog posts.
Implement full email notification system for contact forms.
Expand the admin panel with analytics and user management features.
