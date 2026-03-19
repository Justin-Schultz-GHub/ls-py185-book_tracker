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
        with open('schema.sql', 'r') as f:
            sql = f.read()

        with self._database_connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)

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

    def create_new_user(self, username, hashed_password):
        query = '''
                INSERT INTO users (username, password_hash)
                values (%s, %s)
                '''
        logger.info('Executing query: %s', query)

        with self._database_connect() as connection:
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, (username, hashed_password,))

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

    def get_user_by_username(self, username):
        query = '''
                SELECT * FROM users
                WHERE username = (%s);
                '''
        logger.info('Executing query: %s', query)

        with self._database_connect() as connection:
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, (username,))
                result = cursor.fetchone()

        return result

    def get_all_books(self):
        query = '''
                SELECT b.id, b.title, array_agg(g.name) AS genres
                FROM books b
                JOIN books_genres bg ON b.id = bg.book_id
                JOIN genres g ON bg.genre_id = g.id
                GROUP BY b.id, b.title
                ORDER BY b.title;
                '''
        logger.info('Executing query: %s', query)

        with self._database_connect() as connection:
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query)
                result = cursor.fetchall()

        return result

    def get_book_by_id(self, book_id):
        query = '''
                SELECT * FROM books
                WHERE id = (%s);
                '''
        logger.info('Executing query: %s', query)

        with self._database_connect() as connection:
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, (book_id,))
                result = cursor.fetchone()

        return result

    def user_book_status(self, user_id, book_id):
        query = '''
                SELECT status, score, memo FROM users_books
                WHERE user_id = (%s) and book_id = (%s);
                '''
        logger.info('Executing query: %s', query)

        with self._database_connect() as connection:
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, (user_id, book_id,))
                return cursor.fetchone()

    def add_to_book_list(self, user_id, book_id, status, score, memo):
        query = '''
                SELECT 1 FROM users_books
                WHERE user_id = (%s) and book_id = (%s);
                '''
        logger.info('Executing query: %s', query)

        with self._database_connect() as connection:
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, (user_id, book_id,))
                exists = cursor.fetchone()

        if exists:
            query = '''
                    UPDATE users_books
                    SET status = %s, score = %s, memo = %s
                    WHERE user_id = %s AND book_id = %s;
                    '''
            logger.info('Executing query: %s', query)

            with self._database_connect() as connection:
                with connection.cursor(cursor_factory=DictCursor) as cursor:
                    cursor.execute(query, (status, score, memo, user_id, book_id,))
        else:
            query = '''
                    INSERT INTO users_books (user_id, book_id, status, score, memo)
                    values (%s, %s, %s, %s, %s);
                    '''
            logger.info('Executing query: %s', query)

            with self._database_connect() as connection:
                with connection.cursor(cursor_factory=DictCursor) as cursor:
                    cursor.execute(query, (user_id, book_id, status, score, memo,))

    def get_user_book_list(self, user_id, order_by, order_dir, status):
        allowed_columns = ('title', 'score')
        allowed_orders = ('asc', 'desc')

        if order_by not in allowed_columns:
            order_by = 'title'

        if order_dir not in allowed_orders:
            order_dir = 'desc'

        query = f'''
                SELECT * FROM books as b
                JOIN users_books as ub
                ON b.id = ub.book_id
                '''
        where_clauses = ['user_id = %s']
        params = [user_id]

        if status != 'All':
            where_clauses.append('status = (%s)')
            params.append(status)

        query += ' WHERE ' + ' AND '.join(where_clauses)

        if order_by == 'score':
            query += f' ORDER BY {order_by} {order_dir}, title'
        else:
            query += f' ORDER BY {order_by} {order_dir}'

        logger.info('Executing query: %s', query)

        with self._database_connect() as connection:
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, tuple(params))
                result = cursor.fetchall()

        return result

    def remove_from_book_list(self, user_id, book_id):
        query = '''
                DELETE FROM users_books
                WHERE user_id = (%s) and book_id = (%s);
                '''
        logger.info('Executing query: %s', query)

        with self._database_connect() as connection:
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, (user_id, book_id,))