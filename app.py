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