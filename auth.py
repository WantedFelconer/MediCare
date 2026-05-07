from flask import Blueprint, flash, render_template, request, session, redirect, url_for
print("auth.py is loading...")

auth_bp = Blueprint('auth',__name__,template_folder='templates')

mysql = None

# connecting mysql instance from main app to auth
def loadsql(mysql_instance):
    global mysql
    mysql = mysql_instance

@auth_bp.route('/login', methods = ['POST','GET'])
def login():
    if request.method=='POST':
        email = request.form['email']
        password = request.form['password']
        db = mysql.connection.cursor()
        db.execute('SELECT user_id,name,password,role FROM USER WHERE email=%s',(email,))
        db_info = db.fetchone()
        db.close()
        if db_info is None:
            return "No user found"
        else:
            if password==db_info[2]:
                session['user_id'] = db_info[0]
                session['username'] = db_info[1]
                session['password'] = db_info[2]
                session['role'] = db_info[3]
                role = db_info[3]
                if role=='admin':
                    return redirect(url_for('auth.admin_dashboard'))
                elif role=='doctor':
                    return redirect(url_for('auth.doctor_dashboard'))
                elif role=='patient':
                    return redirect(url_for('auth.patient_dashboard'))   
    return render_template('login.html')

@auth_bp.route('/doctor_dashboard', methods=['GET', 'POST'])
def doctor_dashboard():
    if 'username' not in session or session['role'] != 'doctor':
        return redirect(url_for('auth.login'))
    
    search_results = None
    if request.method == 'POST':
        patient_name = request.form.get('patient_name')
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT user_id, name FROM user WHERE name LIKE %s AND role = 'patient'", ("%" + patient_name + "%",))
        search_results = cursor.fetchall()
        cursor.close()
        
    return render_template('doctor_dashboard.html', search_results=search_results)

@auth_bp.route('/view_patient_profile/<int:patient_id>')
def view_patient_profile(patient_id):
    if 'username' not in session or session['role'] != 'doctor':
        return redirect(url_for('auth.login'))
    
    db = mysql.connection.cursor()
    # Fetch patient details
    db.execute("""
        SELECT u.user_id, u.name, p.sex, p.age, p.medical_records 
        FROM user u 
        LEFT JOIN patient p ON u.user_id = p.user_id 
        WHERE u.user_id = %s
    """, (patient_id,))
    profile = db.fetchone()

    # Count how many times THIS patient has booked with THIS doctor
    db.execute("""
        SELECT COUNT(*) FROM appointments 
        WHERE patient_id = %s AND doctor_id = %s
    """, (patient_id, session['user_id']))
    appt_count = db.fetchone()[0]
    
    db.close()
    return render_template('patient_profile.html', profile=profile, appt_count=appt_count)

@auth_bp.route('/complete_consultation/<int:appt_id>')
def complete_consultation(appt_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE appointments SET status = 'completed' WHERE appointment_id = %s", (appt_id,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('auth.doctor_dashboard'))

@auth_bp.route('/patient_dashboard', methods=['POST','GET'])
def patient_dashboard():
    if 'username' not in session or session['role'] != 'patient':
        return redirect(url_for('auth.login'))
    
    search_results = None
    if request.method == 'POST':
        query = request.form.get('doctor_name')
        db = mysql.connection.cursor()
        # Search doctors by name and join with doctor table for specialty/degree
        db.execute("""
            SELECT u.user_id, u.name, d.speciality, d.degree 
            FROM user u 
            JOIN doctor d ON u.user_id = d.user_id 
            WHERE u.name LIKE %s AND u.role = 'doctor'
        """, ("%" + query + "%",))
        search_results = db.fetchall()
        db.close()

    # Note: Make sure your template filename is search_page.html
    return render_template('search_page.html', search_results=search_results)

@auth_bp.route('/search_doctor_by_name', methods=['POST'])
def search_doctor_by_name():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    doctor_name = request.form.get('doctor_name')
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT user_id FROM user WHERE name LIKE %s AND role = 'doctor' LIMIT 1", ("%" + doctor_name + "%",))
    result = cursor.fetchone()
    cursor.close()
    if result:
        return redirect(url_for('auth.doctor_profile', user_id=result[0]))
    return redirect(url_for('auth.patient_dashboard'))

@auth_bp.route('/search_page', methods=['POST','GET'])
def search_page():
    # This acts as the main patient portal
    return redirect(url_for('auth.patient_dashboard'))

@auth_bp.route('/doctor_profile/<int:user_id>')
def doctor_profile(user_id):
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    db = mysql.connection.cursor()
    db.execute("""
        SELECT u.user_id, u.name, u.email, d.sex, d.speciality, d.degree, d.experience
        FROM user u
        LEFT JOIN doctor d ON u.user_id = d.user_id
        WHERE u.user_id = %s
    """, (user_id,))
    row = db.fetchone()
    db.close()
    if not row:
        return "Doctor not found", 404
    doctor = {"user_id": row[0], "name": row[1], "email": row[2], "sex": row[3], "speciality": row[4], "degree": row[5], "experience": row[6]}
    return render_template('doctor_profile.html', doctor=doctor)

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@auth_bp.route('/register',methods=['POST','GET'])
def register():
    if request.method=='POST':
        username = request.form['name']
        password = request.form['password']
        email = request.form['email']
        role = 'doctor' if email.endswith('@medicare.com') else 'patient'
        db = mysql.connection.cursor()
        db.execute('INSERT INTO USER(name,email,password,role) VALUES (%s,%s,%s,%s)',(username,email,password,role))
        mysql.connection.commit()
        db.close()
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/admin_dashboard')
def admin_dashboard():
    db = mysql.connection.cursor()
    db.execute("SELECT user_id, name, email, role FROM user")
    users = db.fetchall()
    db.close()
    return render_template('admin_dashboard.html', users=users)

@auth_bp.route('/add_user', methods=['POST'])
def add_user():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    role = request.form['role']
    db = mysql.connection.cursor()
    db.execute('INSERT INTO USER(name,email,password,role) VALUES (%s,%s,%s,%s)', (name, email, password, role))
    mysql.connection.commit()
    db.close()
    return redirect(url_for('auth.admin_dashboard'))

@auth_bp.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    db = mysql.connection.cursor()
    db.execute('DELETE FROM USER WHERE user_id=%s', (user_id,))
    mysql.connection.commit()
    db.close()
    return redirect(url_for('auth.admin_dashboard'))

@auth_bp.route('/my_profile', methods=['GET', 'POST'])
def my_profile():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    user_id = session['user_id']
    role = session['role']
    db = mysql.connection.cursor()
    if request.method == 'POST':
        name = request.form['name']
        sex = request.form['sex']
        db.execute("UPDATE user SET name=%s WHERE user_id=%s", (name, user_id))
        if role == 'doctor':
            speciality, degree, experience = request.form['speciality'], request.form['degree'], request.form['experience']
            db.execute("SELECT * FROM doctor WHERE user_id=%s", (user_id,))
            if db.fetchone():
                db.execute("UPDATE doctor SET name=%s, sex=%s, speciality=%s, degree=%s, experience=%s WHERE user_id=%s", (name, sex, speciality, degree, experience, user_id))
            else:
                db.execute("INSERT INTO doctor(user_id, name, sex, speciality, degree, experience) VALUES (%s,%s,%s,%s,%s,%s)", (user_id, name, sex, speciality, degree, experience))
        elif role == 'patient':
            age, records = request.form['age'], request.form['medical_records']
            db.execute("SELECT * FROM patient WHERE user_id=%s", (user_id,))
            if db.fetchone():
                db.execute("UPDATE patient SET name=%s, sex=%s, age=%s, medical_records=%s WHERE user_id=%s", (name, sex, age, records, user_id))
            else:
                db.execute("INSERT INTO patient(user_id, name, sex, age, medical_records) VALUES (%s,%s,%s,%s,%s)", (user_id, name, sex, age, records))
        mysql.connection.commit()
    if role == 'doctor':
        db.execute("SELECT u.user_id, u.name, d.sex, d.speciality, d.degree, d.experience FROM user u LEFT JOIN doctor d ON u.user_id = d.user_id WHERE u.user_id=%s", (user_id,))
    else:
        db.execute("SELECT u.user_id, u.name, p.sex, p.age, p.medical_records FROM user u LEFT JOIN patient p ON u.user_id = p.user_id WHERE u.user_id=%s", (user_id,))
    profile = db.fetchone()
    db.close()
    return render_template('my_profile.html', profile=profile, role=role)

@auth_bp.route('/category/<speciality>')
def category_search(speciality):
    db = mysql.connection.cursor()
    db.execute("SELECT u.user_id, u.name, d.speciality, d.degree FROM user u JOIN doctor d ON u.user_id = d.user_id WHERE d.speciality = %s", (speciality,))
    doctors = db.fetchall()
    db.close()
    return render_template('search_results.html', doctors=doctors, speciality=speciality)

@auth_bp.route('/appoint', methods=['GET', 'POST'])
def appoint():
    if 'user_id' not in session: return redirect(url_for('auth.login'))
    cursor = mysql.connection.cursor()
    doctor_id = request.args.get('doctor_id')
    if request.method == 'POST':
        doctor_id = request.form.get('doctor_id')
        cursor.execute('INSERT INTO appointments (patient_id, doctor_id, appt_date, appt_time, reason, symptoms, status) VALUES (%s, %s, %s, %s, %s, %s, "pending")',
                    (session['user_id'], doctor_id, request.form.get('date'), request.form.get('time'), request.form.get('reason'), request.form.get('symptoms')))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('auth.patient_dashboard'))
    return render_template('appoint.html', doctor_id=doctor_id)

@auth_bp.route('/doctor_notifications')
def doctor_notifications():
    if session.get('role') != 'doctor':
        return redirect(url_for('auth.login'))
    
    cursor = mysql.connection.cursor()
    # Filter by visibility for doctor
    cursor.execute("""
        SELECT a.appointment_id, u.name, a.appt_date, a.appt_time, a.reason, a.status 
        FROM appointments a 
        JOIN user u ON a.patient_id = u.user_id 
        WHERE a.doctor_id = %s AND a.is_visible_to_doctor = 1 
        ORDER BY a.appt_date DESC
    """, (session['user_id'],))
    appointments = cursor.fetchall()
    cursor.close()
    return render_template('doctor_notifications.html', appointments=appointments)

@auth_bp.route('/remove_doctor_notification/<int:appt_id>')
def remove_doctor_notification(appt_id):
    if session.get('role') != 'doctor': return redirect(url_for('auth.login'))
    
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE appointments SET is_visible_to_doctor = 0 WHERE appointment_id = %s AND doctor_id = %s", (appt_id, session['user_id']))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('auth.doctor_notifications'))

@auth_bp.route('/clear_all_doctor_notifications')
def clear_all_doctor_notifications():
    if session.get('role') != 'doctor': return redirect(url_for('auth.login'))
    
    cursor = mysql.connection.cursor()
    # Hide all 'paid' and 'rejected' appointments from doctor's list
    cursor.execute("""
        UPDATE appointments 
        SET is_visible_to_doctor = 0 
        WHERE doctor_id = %s AND (status = 'paid' OR status = 'rejected')
    """, (session['user_id'],))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('auth.doctor_notifications'))

@auth_bp.route('/update_appointment/<int:id>/<action>')
def update_appointment(id, action):
    status = 'accepted' if action == 'accept' else 'rejected'
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE appointments SET status=%s WHERE appointment_id=%s", (status, id))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('auth.doctor_notifications'))

@auth_bp.route('/patient_notifications')
def patient_notifications():
    if session.get('role') != 'patient': 
        return redirect(url_for('auth.login'))
    
    cursor = mysql.connection.cursor()
    # Updated query: Only fetch visible appointments
    cursor.execute("""
        SELECT a.appointment_id, u.name, a.appt_date, a.appt_time, a.status 
        FROM appointments a 
        JOIN user u ON a.doctor_id = u.user_id 
        WHERE a.patient_id = %s AND a.is_visible_to_patient = 1 
        ORDER BY a.appt_date DESC
    """, (session['user_id'],))
    appointments = cursor.fetchall()
    cursor.close()
    return render_template('patient_notifications.html', appointments=appointments)

@auth_bp.route('/remove_notification/<int:appt_id>')
def remove_notification(appt_id):
    if 'user_id' not in session: return redirect(url_for('auth.login'))
    
    cursor = mysql.connection.cursor()
    # Set visibility to 0 (False) so it's hidden from the list
    cursor.execute("UPDATE appointments SET is_visible_to_patient = 0 WHERE appointment_id = %s AND patient_id = %s", (appt_id, session['user_id']))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('auth.patient_notifications'))

@auth_bp.route('/clear_all_paid_notifications')
def clear_all_paid_notifications():
    if 'user_id' not in session: return redirect(url_for('auth.login'))
    
    cursor = mysql.connection.cursor()
    # Hide ALL appointments that are marked as 'paid'
    cursor.execute("""
        UPDATE appointments 
        SET is_visible_to_patient = 0 
        WHERE patient_id = %s AND status = 'paid'
    """, (session['user_id'],))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('auth.patient_notifications'))

@auth_bp.route('/payment/<int:appointment_id>', methods=['GET', 'POST'])
def payment(appointment_id):
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO payments (appointment_id, amount, vat, total, status) VALUES (%s, 500, 75, 575, 'paid')", (appointment_id,))
        cursor.execute("UPDATE appointments SET status='paid' WHERE appointment_id=%s", (appointment_id,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('auth.invoice', appointment_id=appointment_id))
    return render_template('payment.html', appointment_id=appointment_id)

@auth_bp.route('/invoice/<int:appointment_id>')
def invoice(appointment_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT p.amount, p.vat, p.total, u.name FROM payments p JOIN appointments a ON p.appointment_id = a.appointment_id JOIN user u ON a.doctor_id = u.user_id WHERE p.appointment_id = %s", (appointment_id,))
    data = cursor.fetchone()
    cursor.close()
    return render_template('invoice.html', data=data) 

