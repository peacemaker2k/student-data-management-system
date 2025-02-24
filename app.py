import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
import random, smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import pandas as pd
from flask import send_file
import io

app = Flask(__name__)
app.secret_key = os.urandom(24)

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'sanjayjaya2000@gmail.com'   # Replace with your email
EMAIL_PASSWORD = 'mxya ounl yjng mvuo'   # Use app-specific password for Gmail

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('student_management.db')
    conn.row_factory = sqlite3.Row
    return conn

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp(email, otp):
    subject = "Your OTP for Editing Student Details"
    body = f"Your OTP is {otp}. It is valid for 5 minutes."
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, email, msg.as_string())
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

import pandas as pd
from flask import send_file
import io

@app.route('/export_students')
def export_students():
    if 'username' not in session or session['username'] != 'admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('login', user='admin'))

    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()

    # Convert student data to DataFrame
    df = pd.DataFrame(students, columns=students[0].keys() if students else [])

    # ✅ Remove the 'password' column if it exists
    if 'password' in df.columns:
        df = df.drop(columns=['password'])

    # Save to in-memory buffer
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Students')

    output.seek(0)
    return send_file(
        output, 
        as_attachment=True, 
        download_name='students_list.xlsx', 
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@app.route('/request_otp/<register_no>', methods=['GET', 'POST'])
def request_otp(register_no):
    if 'username' not in session or session['username'] != register_no:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('login', user='student'))

    conn = get_db_connection()
    student = conn.execute('SELECT email FROM students WHERE register_no = ?', (register_no,)).fetchone()
    conn.close()

    if student:
        otp = generate_otp()
        session['otp'] = otp
        session['otp_expiry'] = (datetime.now() + timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M:%S')

        if send_otp(student['email'], otp):
            flash('An OTP has been sent to your registered email.', 'info')
            return redirect(url_for('verify_otp', register_no=register_no))
        else:
            flash('Failed to send OTP. Please try again.', 'danger')
    else:
        flash('Student not found.', 'danger')

    return redirect(url_for('dashboard'))

@app.route('/verify_otp/<register_no>', methods=['GET', 'POST'])
def verify_otp(register_no):
    if 'username' not in session or session['username'] != register_no:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('login', user='student'))

    if request.method == 'POST':
        entered_otp = request.form.get('otp')
        otp_expiry = datetime.strptime(session.get('otp_expiry', ''), '%Y-%m-%d %H:%M:%S')

        if datetime.now() > otp_expiry:
            flash('OTP has expired. Please request a new one.', 'warning')
            return redirect(url_for('request_otp', register_no=register_no))

        if entered_otp == session.get('otp'):
            session['otp_verified'] = True
            flash('OTP verified successfully.', 'success')
            return redirect(url_for('edit_student', register_no=register_no))
        else:
            flash('Invalid OTP. Please try again.', 'danger')

    return render_template('verify_otp.html')


# Home Route
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login/<user>', methods=['GET', 'POST'])
def login(user):
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Admin login check
        if user == 'admin' and username == 'admin' and password == 'secret':
            session['username'] = 'admin'
            return redirect(url_for('dashboard'))
        
        # Student login check
        if user == 'student':
            conn = get_db_connection()
            student = conn.execute(
                'SELECT * FROM students WHERE register_no = ? AND password = ?', 
                (username, password)
            ).fetchone()
            conn.close()
            
            if student:
                session['username'] = username
                return redirect(url_for('dashboard'))
        
        flash('Invalid credentials', 'danger')

    return render_template('login.html',user=user)

# After login
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login', user='admin'))  # Default to admin login if not logged in

    user_role = 'student' if session['username'] != 'admin' else 'admin'
    return render_template('dashboard.html', user_role=user_role)

# Logout Route
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

# Add Student Route (Admin Only)
@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    # Allow access only to admin users
    if 'username' not in session or session['username'] != 'admin':
        flash('Unauthorized access. Please log in as admin.', 'danger')
        return redirect(url_for('login', user='admin'))

    if request.method == 'POST':
        # Extract form data
        name = request.form.get('name')
        register_no = request.form.get('register_no')
        roll_no = request.form.get('roll_no')
        department = request.form.get('department')
        year = request.form.get('year')
        dob = request.form.get('dob')
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        address = request.form.get('address')
        father_name = request.form.get('father_name')
        father_occupation = request.form.get('father_occupation')
        mother_name = request.form.get('mother_name')
        mother_occupation = request.form.get('mother_occupation')
        blood_group = request.form.get('blood_group')

        # ✅ Check if all fields are filled
        if not all([name, register_no, roll_no, department, year, dob, email, mobile, address, father_name, father_occupation, mother_name, mother_occupation, blood_group]):
            flash('⚠ All fields are required!', 'warning')
            return render_template('add_student.html')

        conn = get_db_connection()
        try:
            # ✅ Insert data into the database
            conn.execute('''
                INSERT INTO students (
                    register_no, name, roll_no, department, year, dob, 
                    email, mobile, address, father_name, father_occupation, 
                    mother_name, mother_occupation, blood_group
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                register_no, name, roll_no, department, year, dob, 
                email, mobile, address, father_name, father_occupation, 
                mother_name, mother_occupation, blood_group
            ))
            conn.commit()
            flash('✅ Student added successfully!', 'success')
            return redirect(url_for('students_list'))

        except sqlite3.IntegrityError:
            # Handles duplicate register_no entries due to PRIMARY KEY constraint
            flash(f'❌ A student with Register No: {register_no} already exists.', 'danger')
            return render_template('add_student.html')

        finally:
            conn.close()

    return render_template('add_student.html')

# View All Students Route (Admin Only)
@app.route('/students_list')
def students_list():
    if 'username' not in session or session['username'] != 'admin':
        return redirect(url_for('login'))

    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return render_template('students_list.html', students=students)

# View Student Details (Student or Admin)
@app.route('/student_details/<register_no>', methods=['GET', 'POST'])
def student_details(register_no):
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE register_no = ?', (register_no,)).fetchone()
    conn.close()

    if student:
        return render_template('student_details.html', student=student)
    else:
        flash('Student not found!', 'danger')
        return redirect(url_for('students_list'))

# Edit student details route
@app.route('/edit_student/<register_no>', methods=['GET', 'POST'])
def edit_student(register_no):
    if 'username' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))

    is_admin = session['username'] == 'admin'
    is_student = session['username'] == register_no

    # ❌ If neither admin nor the student themselves, block access
    if not is_admin and not is_student:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('dashboard'))

    # 🛡️ ✅ OTP is required ONLY for students, NOT for admin
    if is_student and not is_admin and not session.get('otp_verified'):
        # flash('Please verify OTP before editing your details.', 'warning')
        return redirect(url_for('request_otp', register_no=register_no))

    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE register_no = ?', (register_no,)).fetchone()

    if not student:
        flash('Student not found.', 'danger')
        return redirect(url_for('students_list'))

    if request.method == 'POST':
        updated_data = (
            request.form['name'], request.form['roll_no'], request.form['department'],
            request.form['year'], request.form['dob'], request.form['email'],
            request.form['mobile'], request.form['address'], request.form['father_name'],
            request.form['father_occupation'], request.form['mother_name'],
            request.form['mother_occupation'], request.form['blood_group'],
            request.form['password'], register_no
        )

        conn.execute('''
            UPDATE students SET
                name = ?, roll_no = ?, department = ?, year = ?, dob = ?, email = ?, 
                mobile = ?, address = ?, father_name = ?, father_occupation = ?, 
                mother_name = ?, mother_occupation = ?, blood_group = ?, password = ?
            WHERE register_no = ?
        ''', updated_data)
        conn.commit()
        conn.close()

        # ✅ Clear OTP session after student updates details
        if is_student:
            session.pop('otp_verified', None)
            session.pop('otp', None)
            session.pop('otp_expiry', None)

        flash('Student details updated successfully.', 'success')
        return redirect(url_for('student_details', register_no=register_no))

    return render_template('edit_student.html', student=student)

# Delete Student (Admin Only)
@app.route('/delete_student/<register_no>')
def delete_student(register_no):
    if 'username' not in session or session['username'] != 'admin':
        return redirect(url_for('login'))

    conn = get_db_connection()
    conn.execute('DELETE FROM students WHERE register_no = ?', (register_no,))
    conn.commit()
    conn.close()
    flash('Student deleted successfully!', 'success')
    return redirect(url_for('students_list'))

if __name__ == '__main__':  # ✅ Correct
    app.run(debug=True)
