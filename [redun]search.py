from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session

search_bp = Blueprint('search', __name__, template_folder='templates')
mysql = None

def loadsql(mysql_instance):
    global mysql
    mysql = mysql_instance

@search_bp.route('/search_page')
def search_page():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    return render_template('search_page.html')

# Live suggestions endpoint
@search_bp.route('/search_suggestions')
def search_suggestions():
    query = request.args.get('q', '')
    role = request.args.get('role', 'DOCTOR')  # default doctor
    db = mysql.connection.cursor()
    db.execute("SELECT user_id, name FROM user WHERE name LIKE %s AND role = %s LIMIT 5", (f"%{query}%", role))
    results = db.fetchall()
    db.close()
    return jsonify([{"id": r[0], "name": r[1]} for r in results])

# Final search submit
@search_bp.route('/search', methods=['POST'])
def search():
    name_query = request.form['name']
    role = request.form.get('role', 'DOCTOR')

    db = mysql.connection.cursor()

    # Exact match first
    db.execute("SELECT user_id, name, email, role FROM user WHERE name = %s AND role = %s LIMIT 1", (name_query, role))
    exact_match = db.fetchone()

    # Similar matches (excluding exact match), limit 9
    db.execute("SELECT user_id, name, email, role FROM user WHERE name LIKE %s AND role = %s AND name != %s LIMIT 9",
               (f"%{name_query}%", role, name_query))
    similar_matches = db.fetchall()

    db.close()

    return render_template(
        'search_results.html',
        exact_match=exact_match,
        similar_matches=similar_matches,
        query=name_query,
        role=role
    )


# Profile redirect
@search_bp.route('/profile/<int:user_id>')
def profile(user_id):
    db = mysql.connection.cursor()
    db.execute("SELECT user_id, name, email, role FROM user WHERE user_id = %s", (user_id,))
    user = db.fetchone()
    db.close()
    return render_template('doctor_profile.html', user=user)
