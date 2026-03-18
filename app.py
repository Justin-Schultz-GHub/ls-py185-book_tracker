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
app.config['DATABASE'] = 'book_tracker'
app.secret_key=secrets.token_hex(32)

@app.before_request
def initialize_persistence():
    dbname = app.config.get('DATABASE', os.environ.get('DATABASE', 'book_tracker'))
    g.storage = DatabasePersistence(dbname=dbname)
    g.session = SessionPersistence(session)

# Route Hooks
@app.route('/')
def index():
    if "user_id" in session:
        return redirect(url_for('home'))

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

        return redirect(url_for('home'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = g.storage.get_user_by_username(username)

        if user and check_password_hash(user['password_hash'], password):
            g.session.login(user['id'])
            flash('Successfully logged in', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username and password combination', 'error')
            return render_template('login.html', username=username)

    return render_template('login.html')

@app.route('/logout')
def logout():
    g.session.logout()

    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/books')
def books():
    books = g.storage.get_all_books()
    print(type(books))
    return render_template('books.html', books=books)

@app.route('/book/<int:book_id>')
def book(book_id):
    book = g.storage.get_book_by_id(book_id)
    user_book = None

    if session.get('user_id'):
        user_book = g.storage.user_book_status(session['user_id'], book_id)

    return render_template('book.html', book=book, user_book=user_book)

@app.route('/book_list')
def book_list():
    return render_template('book_list.html')

@app.route('/add_to_book_list/<int:book_id>', methods=['GET', 'POST'])
def add_to_book_list(book_id):
    status = request.form['status']
    score = str(request.form['score'])

    g.storage.add_to_book_list(session['user_id'], book_id, status, score)

    return redirect(url_for('book', book_id=book_id))

if __name__ == "__main__":
    if os.environ.get('FLASK_ENV') == 'production':
        app.run(debug=False)
    else:
        app.run(debug=True, port=8080)