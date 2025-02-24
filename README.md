Student Management System with OTP Verification

📖 Overview

The Student Management System is a web-based application built with Flask and SQLite to manage student records efficiently. It allows administrators to add, edit, delete, and view student details, while students can log in to view and edit their profiles with OTP verification for added security. The system features a clean, responsive interface accessible across all devices and major browsers.


---

🚀 Features

Admin Panel: Manage student data (add, edit, delete, view) with ease.

Student Access: Students can log in to view and edit their details securely.

OTP Verification: Enhanced security for students when editing details.

Responsive Design: Fully accessible across desktops, tablets, and smartphones.

Cross-Browser Compatibility: Works seamlessly on all major browsers.

Secure Sessions: User authentication with session management.

User-Friendly Interface: Intuitive navigation and clean design.



---

🛠️ Tech Stack

Backend: Flask (Python)

Database: SQLite

Frontend: HTML, CSS, Bootstrap (for responsive design), Jinja2 Templates

Email Service: SMTP (Gmail) for OTP emails



---

📥 Installation & Setup

1. Clone the Repository:
git clone <repository_url>


2. Create a Virtual Environment:
python -m venv venv


3. Activate the Environment:

Windows: venv\Scripts\activate

macOS/Linux: source venv/bin/activate



4. Install Dependencies:
pip install -r requirements.txt


5. Configure Environment Variables:
Create a .env file and add:

FLASK_APP=app.py
FLASK_ENV=development
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_specific_password


6. Run the Application:
flask run


7. Access the App:
Visit http://127.0.0.1:5000/ in your browser.




---

🔑 Usage

Admin Login:

Username: admin

Password: secret


Student Access:

Students log in with their register number and password.

An OTP will be sent to the registered email for editing details.




---

📝 Database Schema (students table)

register_no (Primary Key)

name

roll_no

department

year

dob

email

mobile

address

father_name

father_occupation

mother_name

mother_occupation

blood_group

password



---

📧 Email & OTP Setup

Configure SMTP using Gmail with an app-specific password.

OTP is valid for 5 minutes for enhanced security.



---

📱 Responsiveness & Accessibility

Fully Responsive: The application adapts to all screen sizes, ensuring usability on desktops, tablets, and mobile devices.

Cross-Browser Support: Compatible with Chrome, Firefox, Edge, Safari, and Opera.

Accessible Design: Clear navigation, readable fonts, and proper contrast for a user-friendly experience.



---

💡 Future Enhancements

Password reset via email.

Data export to Excel/PDF.

Role-based access control.

Dark mode support.



---

🙌 Contributing

Contributions are welcome! Feel free to fork the repo, make changes, and submit a pull request.


---

📄 License

This project is licensed under the MIT License.


---

📝 Acknowledgments

Flask & Python Community

Bootstrap for responsive UI

Gmail SMTP for email services

