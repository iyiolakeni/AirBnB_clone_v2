#!/usr/bin/python3
"""DBStorage class for HBNB project"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from os import getenv

class DBStorage:
    """DBStorage class for HBNB project"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize DBStorage instance"""
        user = getenv('HBNB_MYSQL_USER')
        pwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(user, pwd, host, db),
                                      pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query objects from the database
        if cls is none, query all types of objects 
        
        Return:
            Dictionary of queried class  
        """
        from models import storage
        if cls:
            objs = self.__session.query(cls).all()
        else:
            classes = ['User', 'State', 'City', 'Amenity', 'Place', 'Review']
            objs = []
            for cls_name in classes:
                cls = storage.all_classes()[cls_name]
                objs.extend(self.__session.query(cls).all())

        return {obj.__class__.__name__ + '.' + obj.id: obj for obj in objs}

    def new(self, obj):
        """Add the object to the current database session"""
        if obj:
            self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables and a scoped session on the current database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def close(self):
        """Close the session"""
        self.__session.close()
