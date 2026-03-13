import secrets
import os
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

# Route Hooks
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    if os.environ.get('FLASK_ENV') == 'production':
        app.run(debug=False)
    else:
        app.run(debug=True, port=8080)