from sqlalchemy import (
    create_engine,
    Column,
    ForeignKey,
    Integer,
    String,
    TIMESTAMP,
    Boolean,
    Enum,
    ARRAY,
    FLOAT,
    JSON
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

user = os.environ.get("POSTGRES_USER")
password = os.environ.get("POSTGRES_PASSWORD")
host = os.environ.get("POSTGRES_HOST")
db = os.environ.get("POSTGRES_DB")
is_prod = os.environ.get("K_SERVICE")

print('trying to connect to sql server', is_prod)
database_connection_url = ''
if not is_prod:
    database_connection_url = "postgresql://" + user + ":" + password + "@" + host + "/" + db
else:
    db_socket_dir = os.environ.get("DB_SOCKET_DIR", "/cloudsql")
    cloud_sql_connection_name = os.environ["CLOUD_SQL_CONNECTION_NAME"]
    unix_socket = "{}/{}".format(
                db_socket_dir,
                cloud_sql_connection_name)
    database_connection_url = "postgresql://" + user + ":" + password + "@/" + db + "?unix_socket=" + cloud_sql_connection_name
    print(database_connection_url, 'url')
engine = create_engine(database_connection_url)
print('connected to sql server')


class Event(Base):
    __tablename__ = "event"

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey("organization.id"))
    location_id = Column(Integer, nullable=True)
    description = Column(String)
    name = Column(String)
    cover_image_url = Column(String, nullable=True)
    cover_image_hash = Column(String, nullable=True)
    poster_image_url = Column(String, nullable=True)
    poster_image_hash = Column(String, nullable=True)
    profile_image_url = Column(String, nullable=True)
    profile_image_hash = Column(String, nullable=True)
    attendee_limit = Column(Integer)
    contact = Column(String, nullable=True)
    registration_due_date = Column(TIMESTAMP, nullable=True)


class EventDuration(Base):
    __tablename__ = "event_duration"

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("event.id"))
    start = Column(TIMESTAMP)
    finish = Column(TIMESTAMP)


class Tag(Base):
    __tablename__ = "tag"

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    id = Column(Integer, primary_key=True)
    name = Column(String)


class EventTag(Base):
    __tablename__ = "event_tag"

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("event.id"))
    tag_id = Column(Integer, ForeignKey("tag.id"))


class EventRecommendation(Base):
    __tablename__ = "event_vector"
    
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
    
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("event.id"))
    event_vector = Column(ARRAY(FLOAT))
    score = Column(JSON)



Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)