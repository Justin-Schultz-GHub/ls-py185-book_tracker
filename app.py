import secrets
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask import (
                    flash,
                    Flask,
                    render_template,
                    redirect,
                    request,
                    session,
                    url_for,
                    g,
                    )

from persistence.database_persistence import (
                                            DatabasePersistence,
                                            )

from persistence.session_persistence import (
                                            SessionPersistence,
                                            )

app = Flask(__name__)
app.config['DATABASE'] = 'flashcards'
app.secret_key=secrets.token_hex(32)

@app.before_request
def initialize_persistence():
    dbname = app.config.get('DATABASE', os.environ.get('DATABASE', 'book_tracker'))
    g.storage = DatabasePersistence(dbname=dbname)

# Route Hooks
@app.route('/')
def index():
    if "user_id" in session:
        return redirect(url_for('books'))

    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if g.storage.username_exists(username):
            flash('This username is already taken.', 'error')
            return render_template('signup.html', username=username)

        if not password:
            flash('Please enter a password.', 'error')
            return render_template('signup.html')

        hashed_password = generate_password_hash(password)
        g.storage.create_new_user(username, hashed_password)
        user_id = g.storage.get_user_id(username)
        session['user_id'] = user_id
        flash('Account created successfully', 'success')

        return redirect(url_for('books'))


    return render_template('signup.html')

@app.route('/books')
def books():
    return render_template('books.html')


if __name__ == "__main__":
    if os.environ.get('FLASK_ENV') == 'production':
        app.run(debug=False)
    else:
        app.run(debug=True, port=8080)