from Post import Post
import sqlite3


class PostDB:

    def __init__(self, namedb):
        self.conn = sqlite3.connect(namedb)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS postdb(
                id INTEGER PRIMARY KEY,
                name TEXT,
                price FLOAT,
                condition TEXT,
                link TEXT DISTINCT,
                subscription TEXT,
                has_delivery TEXT,
                page INTEGER
                );
            """)

    def add_post(self, post):
        self.cursor.execute("""
            INSERT INTO postdb VALUES
            (?, ?, ?, ?, ?, ?, ?, ?)
        """, (self.get_last_id()+1, post.name, post.price, post.condition, post.link, post.subscription, post.has_delivery, post.page))
        self.conn.commit()
    def get_last_id(self):
        self.cursor.execute("""
            SELECT id FROM postdb ORDER BY id DESC LIMIT 1
        """)
        row = self.cursor.fetchone()
        if row is None:
            return 0
        return row[0]