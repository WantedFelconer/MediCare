from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from auth import auth_bp,loadsql

app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'       # MySQL server
app.config['MYSQL_USER'] = 'root'            # MySQL username
app.config['MYSQL_PASSWORD'] = ''  # MySQL password
app.config['MYSQL_DB'] = 'MediCare'        # Database name
app.config['SECRET_KEY'] = 'asdfghjkl'  # Needed for sessions

mysql = MySQL(app)
loadsql(mysql)
app.register_blueprint(auth_bp)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/search_page',methods=['POST','GET'])
def search_page():
    return render_template('search_page.html')

@app.route('/doctor_profile',methods=['POST','GET'])
def doctor_profile():
    return render_template('doctor_profile.html')

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