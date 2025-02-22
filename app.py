import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('student_management.db')
    conn.row_factory = sqlite3.Row
    return conn

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


    # if 'username' in session:
    #     return redirect(url_for('students_list'))
    # return redirect(url_for('login'))

# Login Route
# # @app.route('/login', methods=['GET', 'POST'])
# # def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         # Admin login
#         if username == 'admin' and password == 'secret':
#             session['username'] = 'admin'
#             return redirect(url_for('students_list'))
#         # Student login
#         conn = get_db_connection()
#         student = conn.execute('SELECT * FROM students WHERE register_no = ? AND password = ?', (username, password)).fetchone()
#         conn.close()

#         if student:
#             session['username'] = username
#             return redirect(url_for('student_details', register_no=username))
#         else:
#             flash('Invalid login credentials', 'danger')
#     return render_template('login.html')

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
        return redirect(url_for('login'))
    
    # Check if the user is admin or student
    if session['username'] == 'admin':
        # Admin can edit any student
        conn = get_db_connection()
        student = conn.execute('SELECT * FROM students WHERE register_no = ?', (register_no,)).fetchone()
        conn.close()
    elif session['username'] == register_no:
        # Students can only edit their own details
        conn = get_db_connection()
        student = conn.execute('SELECT * FROM students WHERE register_no = ?', (register_no,)).fetchone()
        conn.close()
    else:
        return redirect(url_for('student_details', register_no=session['register_no']))
    
    if request.method == 'POST':
        # Get updated data from the form
        name = request.form['name']
        roll_no = request.form['roll_no']
        department = request.form['department']
        year = request.form['year']
        dob = request.form['dob']
        email = request.form['email']
        mobile = request.form['mobile']
        address = request.form['address']
        father_name = request.form['father_name']
        father_occupation = request.form['father_occupation']
        mother_name = request.form['mother_name']
        mother_occupation = request.form['mother_occupation']
        blood_group = request.form['blood_group']
        password = request.form['password']

        # Update the student details in the database
        conn = get_db_connection()
        conn.execute('''
            UPDATE students
            SET name = ?, roll_no = ?, department = ?, year = ?, dob = ?, email = ?, mobile = ?, address = ?, 
                father_name = ?, father_occupation = ?, mother_name = ?, mother_occupation = ?, blood_group = ?, password = ?
            WHERE register_no = ?
        ''', (name, roll_no, department, year, dob, email, mobile, address, father_name, father_occupation, 
            mother_name, mother_occupation, blood_group, password, register_no))
        conn.commit()
        conn.close()
        flash('Student details updated successfully!', 'success')
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

if __name__ == 'main':
    app.run(debug=True)