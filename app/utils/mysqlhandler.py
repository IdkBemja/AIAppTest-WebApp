import pymysql
from app.utils.config.env_config import get_db

USER_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(32) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    token VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
"""

JWT_BLACKLIST_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS jwt_blacklist (
    id INT AUTO_INCREMENT PRIMARY KEY,
    token VARCHAR(512) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

def ensure_databases_and_tables():
    db_conf = get_db()
    host = db_conf['host']
    user = db_conf['user']
    password = db_conf['password']
    port = db_conf['port']
    dbname = db_conf['dbname']
    dbname_blacklist = db_conf.get('dbname_blacklist_jwt') or dbname

    dbs = [dbname]
    if dbname_blacklist and dbname_blacklist != dbname:
        dbs.append(dbname_blacklist)

    # Connect to MySQL server (no database selected)
    conn = pymysql.connect(host=host, user=user, password=password, port=port, autocommit=True)
    cursor = conn.cursor()

    # Check and create databases if not exist
    for db in dbs:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db}`;")

    # Create tables in main db
    cursor.execute(f"USE `{dbname}`;")
    cursor.execute(USER_TABLE_SQL)

    # Create tables in blacklist db (if different)
    if dbname_blacklist:
        cursor.execute(f"USE `{dbname_blacklist}`;")
        cursor.execute(JWT_BLACKLIST_TABLE_SQL)

    cursor.close()
    conn.close()