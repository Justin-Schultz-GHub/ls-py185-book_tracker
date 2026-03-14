import os
from contextlib import contextmanager
import psycopg2
from psycopg2.extras import DictCursor
import logging

LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

class DatabasePersistence:
    def __init__(self, dbname=None):
        self.dbname = dbname or os.environ.get('DATABASE') or 'book_tracker'
        self._setup_schema()

    def _setup_schema(self):
        with self._database_connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute('''
                                CREATE TABLE IF NOT EXISTS books (
                                id SERIAL PRIMARY KEY,
                                title TEXT UNIQUE NOT NULL,
                                author TEXT
                                );
                            ''')

                cursor.execute('''
                                CREATE TABLE IF NOT EXISTS genres (
                                id SERIAL PRIMARY KEY,
                                name text UNIQUE NOT NULL
                                );
                            ''')

                cursor.execute('''
                                CREATE TABLE IF NOT EXISTS books_genres
                                book_id INTEGER NOT NULL REFERENCES books(id) ON DELETE CASCADE,
                                genre_id INTEGER NOT NULL REFERENCES genres(id) ON DELETE CASCADE,
                                PRIMARY KEY (book_id, genre_id)
                                );
                            ''')
                cursor.execute('''
                                CREATE INDEX IF NOT EXISTS idx_books_genres_genre_id
                                ON books_genres (genre_id);
                            ''')
                cursor.execute('''
                                CREATE TABLE IF NOT EXISTS users (
                                id SERIAL PRIMARY KEY,
                                username VARCHAR(20) UNIQUE,
                                password_hash TEXT NOT NULL
                                );
                            ''')
                cursor.execute('''
                                CREATE TABLE IF NOT EXISTS users_books (
                                id SERIAL PRIMARY KEY,
                                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                                book_id INTEGER REFERENCES books(id) ON DELETE CASCADE,
                                status TEXT NOT NULL CHECK (status in ('Completed', 'Reading', 'Plan to Read', 'Dropped')),
                                score TEXT
                                );
                            ''')

    @contextmanager
    def _database_connect(self):
        if os.environ.get('FLASK_ENV') == 'production':
            connection = psycopg2.connect(os.environ['DATABASE_URL'])
        else:
            connection = psycopg2.connect(dbname=self.dbname)

        try:
            with connection:
                yield connection
        finally:
            connection.close()

    def username_exists(self, username):
        query = '''
                SELECT 1 FROM users
                WHERE username = (%s);
                '''
        logger.info('Executing query: %s', query)

        with self._database_connect() as connection:
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, (username,))
                result = cursor.fetchone()

        return result is not None

    def create_new_user(self, username, password):
        query = '''
                INSERT INTO users (username, password_hash)
                values (%s, %s)
                '''
        logger.info('Executing query: %s', query)

        with self._database_connect() as connection:
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, (username, password,))

    def get_user_id(self, username):
        query = '''
                SELECT id FROM users
                WHERE username = (%s);
                '''
        logger.info('Executing query: %s', query)

        with self._database_connect() as connection:
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, (username,))
                result = cursor.fetchone()

        return result['id'] if result else None
