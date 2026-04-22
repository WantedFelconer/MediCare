from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL


app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'       # MySQL server
app.config['MYSQL_USER'] = 'root'            # MySQL username
app.config['MYSQL_PASSWORD'] = ''  # MySQL password
app.config['MYSQL_DB'] = 'MediCare'        # Database name
app.config['SECRET_KEY'] = 'asdfghjkl'  # Needed for sessions

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods = ['POST','GET'])
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
                return redirect(url_for('dashboard'))
            
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('login'))

@app.route('/register',methods=['POST','GET'])
def register():
    if request.method=='POST':
        username = request.form['name']
        password = request.form['password']
        email = request.form['email']

        db = mysql.connection.cursor()
        db.execute('INSERT INTO USER(name,email,password,role) VALUES (%s,%s,%s,%s)',(username,email,password,'patient'))
        mysql.connection.commit()
        db.close()
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/search_page',methods=['POST','GET'])
def search_page():
    return render_template('search_page.html')

# @app.route('/doctor_profile',methods=['POST','GET'])
# def doctor_profile():
#     return render_template('doctor_profile.html')

@app.route('/dashboard')
def dashboard():
    db = mysql.connection.cursor()
    db.execute("SELECT user_id, name, email, role FROM user")
    users = db.fetchall()
    db.close()

    # Pass the list of users to the template
    return render_template('dashboard.html', users=users)



if __name__ == "__main__":
    app.run(debug=True)