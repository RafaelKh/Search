import sqlite3
from sqlite3 import Error
from config import SITE_NAME, SITE_PROTOCOL

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_link(conn, link_data):
    sql = ''' INSERT INTO links(path, domain, protocol)
                VALUES(?,?,?) '''
    
    c = conn.cursor()
    c.execute(sql, link_data)
    conn.commit()
    return c.lastrowid


def select_all_links(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM links")
    rows = c.fetchall()
    return rows