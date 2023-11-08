import sqlite3

class DataBase:
    ''' Class for work with database'''

    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()

    def create_tables(self):
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS COUNTRY (
                ID_COUNTRY INTEGER PRIMARY KEY,
                NAME_COUNTRY TEXT UNIQUE
            )
        ''')

        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS ISG (
                ID_ISG INTEGER PRIMARY KEY,
                NAME_ISG TEXT UNIQUE
            )
        ''')

        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS GOODS (
                ID_TOVAR INTEGER PRIMARY KEY,
                NAME_TOVAR TEXT,
                BARCOD TEXT,
                ID_COUNTRY INTEGER,
                ID_ISG INTEGER
            )
        ''')
        self.conn.commit()

    def insert_country(self, name):
        self.cur.execute('INSERT OR IGNORE INTO COUNTRY (NAME_COUNTRY) VALUES (?)', (name,))
        self.conn.commit()

    def insert_isg(self, id, name):
        self.cur.execute('INSERT OR IGNORE INTO ISG (ID_ISG, NAME_ISG) VALUES (?, ?)', (id, name))
        self.conn.commit()

    def insert_good(self, name, barcod, country, isg_id):
        country_id = self.get_country_id(country)
        self.cur.execute('INSERT INTO GOODS (NAME_TOVAR, BARCOD, ID_COUNTRY, ID_ISG) VALUES (?, ?, ?, ?)', (name, barcod, country_id, isg_id))
        self.conn.commit()

    def get_by_table(self, name: str = 'GOODS'):
        result = self.cur.execute(f'SELECT * FROM {name}')
        return result.fetchall()

    def get_country_id(self, country):
        id = self.cur.execute(f"SELECT ID_COUNTRY FROM COUNTRY WHERE NAME_COUNTRY={country!r}").fetchone()
        return str(*id)

    def close(self):
        self.conn.close()
