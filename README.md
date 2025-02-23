## 📖 Project Overview

# student-data-management-system

"A comprehensive Student Management System developed using Python (Flask), SQLite, and Bootstrap. The application enables administrators to add, update, and view student records, while students can log in to view and edit their personal information. Designed for efficiency and ease of use."

---

## 🚀 Features

- **Admin Functionalities:**
  - Add, view, and edit student details.
  - Manage student records securely.
- **Student Functionalities:**
  - Login to view and update personal information.
- **Authentication:**
  - Separate login for Admin and Students.
  - Secure session management.
- **Responsive Design:**
  - Clean UI with Bootstrap 4 support for mobile and desktop.

---

## 🛠️ Technologies Used

- **Backend:** Python (Flask)
- **Database:** SQLite
- **Frontend:** HTML, CSS (Bootstrap), JavaScript
- **Version Control:** Git

---

## 📂 Project Structure

```
student-management-system/
├── app.py              # Main Flask application
├── templates/          # HTML templates
│   ├── home.html
│   ├── login.html
│   ├── dashboard.html
│   ├── add_student.html
│   ├── students_list.html
│   └── edit_student.html
├── static/             # Static files (CSS, JS, images)
├── database.db         # SQLite database
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation
```

---

## 💻 Installation & Setup

### Prerequisites

- Python 3.x installed on your machine.
- Git (optional, for version control).

### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/student-management-system.git
   cd student-management-system
   ```
2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the application:**
   ```bash
   python -m flask run
   ```
5. **Access the application:**
   Open your browser and navigate to `http://localhost:5000`.

---

## 🔑 User Credentials

- **Admin Login:**
  - Username: `admin`
  - Password: `secret`
- **Student Login:**
  - Use the registered student `register_no` and `password`.

---

## 📝 How to Use

1. **Home Page:** Select either Admin or Student login.
2. **Admin:** Can add new students, view student list, and edit student details.
3. **Student:** Can view and update personal details.

---

## 🧪 Testing

- Tested on major browsers (Chrome, Firefox, Edge).
- Ensured responsive design for different screen sizes.
- Validated form inputs for data integrity.

---

## 📄 Future Improvements

- Password reset functionality.
- Role-based permissions.
- Export student data to CSV/PDF.
- Email notifications.

---

## 🧑‍💻 About Me

- Name: Sanjay
- mail to: [sanjayjaya2000@gmail.com](mailto:sanjayjaya2000@gmail.com)
- mobile: 9080337524

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
