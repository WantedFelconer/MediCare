from flask import Blueprint, render_template, request, session, redirect, url_for
print("auth.py is loading...")

auth_bp = Blueprint('auth',__name__,template_folder='templates')

mysql = None

#connecting mysql instance from main app to auth
def loadsql(mysql_instance):
    global mysql
    mysql = mysql_instance

@auth_bp.route('/login', methods = ['POST','GET'])
def login():
    if request.method=='POST':
        email = request.form['email']
        password = request.form['password']

        db = mysql.connection.cursor()
        db.execute('SELECT name,password,role FROM USER WHERE email=%s',(email,))
        db_info = db.fetchone()
        db.close()
        if db_info is None:
            return "No user found"
        else:
            if password==db_info[1]:
                session['username'] = db_info[0]
                session['role'] = db_info[2]
                return redirect(url_for('search_page'))
            
    return render_template('login.html')

@auth_bp.route('/search', methods=['POST'])
def search():
    name_query = request.form['name']  # input field name="name" in your form
    db = mysql.connection.cursor()
    db.execute("SELECT user_id, name, email, role FROM user WHERE name LIKE %s AND role = 'DOCTOR'", (f"%{name_query}%",))
    results = db.fetchall()
    db.close()

    return render_template('search_results.html', results=results, query=name_query)


@auth_bp.route('/logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('auth.login'))

@auth_bp.route('/register',methods=['POST','GET'])
def register():
    if request.method=='POST':
        username = request.form['name']
        password = request.form['password']
        email = request.form['email']

        db = mysql.connection.cursor()
        db.execute('INSERT INTO USER(name,email,password,role) VALUES (%s,%s,%s,%s)',(username,email,password,'patient'))
        mysql.connection.commit()
        db.close()
        return redirect(url_for('auth.login'))

    return render_template('register.html')
