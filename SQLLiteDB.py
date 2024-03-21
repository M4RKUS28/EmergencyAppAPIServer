import sqlite3

limit = 100


class SQLiteDB:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS kv (key TEXT PRIMARY KEY, value TEXT)')

    def put(self, key, value):
        # Check the current number of entries
        self.cursor.execute('SELECT COUNT(*) FROM kv')
        count = self.cursor.fetchone()[0]

        if count >= limit:
            # Fetch the rowid of the oldest entry
            self.cursor.execute('SELECT rowid FROM kv ORDER BY rowid ASC LIMIT 1')
            oldest_rowid = self.cursor.fetchone()[0]
            # Delete the oldest entry
            self.cursor.execute('DELETE FROM kv WHERE rowid = ?', (oldest_rowid,))

        key = str(key)
        value = str(value)
        self.cursor.execute('REPLACE INTO kv (key, value) VALUES (?, ?)', (key, value))
        self.conn.commit()

        return count

    def get(self, key):
        key = str(key)
        self.cursor.execute('SELECT value FROM kv WHERE key = ?', (key,))
        value = self.cursor.fetchone()
        if value:
            return value[0]
        else:
            return None

    def close(self):
        self.conn.close()
