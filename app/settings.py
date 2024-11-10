import os

SERVER_HOST = os.getenv("HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("WEB_PORT", 3500))


MYSQL_DB_NAME = os.getenv("MYSQL_DB_NAME", "appointment_manager")
MYSQL_DB_USER = os.getenv("MYSQL_DB_USER", "root")
MYSQL_DB_PASSWORD = os.getenv("MYSQL_DB_PASSWORD", "paswordd")
MYSQL_DB_PORT = os.getenv("MYSQL_DB_PORT", "3306")
MYSQL_DB_HOST = os.getenv("MYSQL_DB_HOST", "localhost")

MYSQL_CONNECTION = "{}:{}@{}:{}/{}".format(MYSQL_DB_USER, MYSQL_DB_PASSWORD,
                                           MYSQL_DB_HOST, MYSQL_DB_PORT, MYSQL_DB_NAME)