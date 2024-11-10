from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import MYSQL_CONNECTION

DB_URL = "mysql+mysqlconnector://{}".format(MYSQL_CONNECTION)

# env = os.environ.get("env", "dev")
# echo = True if env == "dev" else False

engine = create_engine(DB_URL, pool_pre_ping=True, pool_recycle=3600)
# pool recycle refreshes MySql connection every 1hr for SqlAlchemy, by default mysql has 8hrs of connection
# expire time, i.e. if no query is emitted using connection for more than 8hrs, mysql will terminate the
# connection, but sqlalchemy will use old connection which is terminated by MySql Server,
# hence MySqlConnection Not Available will be raised

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
