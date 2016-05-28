from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from mothball.db.models.base import Base
from mothball.db.base import DatabaseBase

import logging


class SQLConnect(object):

    def __init__(self, address, port, username='bull', password='bullbythehorns', db_type='mysql'):
        self.username = username
        self.password = password
        self.address = address
        self.port = port
        self.session = None
        self.db_type = db_type
        self.engine = None
        self.session = None

    # TODO breakout Mysql and Postgres to child classes that import SQLConenct (DBBase?)

    def _mysql(self):
        self.engine = create_engine('mysql+pymysql://{0}:{1}@{2}:{3}/Backup'.format(self.username,
                                                                               self.password,
                                                                               self.address,
                                                                               self.port))

    def _postgres(self):
        self.engine = create_engine('postgresql://{0}:{1}@{2}:{3}/Backup'.format(self.username,
                                                                                 self.password,
                                                                                 self.address,
                                                                                 self.port))

    def _db_picker(self):
        if self.db_type == 'postgresql':
            self._postgres()
        else:
            self._mysql()

    def connect(self):

        if not self.engine:
            self._db_picker()

        DBSession = sessionmaker()
        DBSession.bind = self.engine

        self.session = DBSession()

    def create_tables(self):

        if not self.engine:
            self._db_picker()

        Base.metadata.create_all(self.engine)


    def close(self):
        self.session.close()

    def update(self, data_object):
        if not self.session:
            logging.warning('No db session has been made to create a record for.  self.connect first.')

        self.session.add(data_object)
        self.session.commit()


