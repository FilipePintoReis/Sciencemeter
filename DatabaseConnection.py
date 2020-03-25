from sqlalchemy import create_engine
from sqlalchemy import Table, Column, String, MetaData
from credentials import username, password

try:
    db_string = "postgresql://{username}:{password}@localhost:5432/science_metre".format(username, password)
except Exception as ex:
    print('Exception was: {0}'.format(ex))

engine = create_engine(db_string)

class PaperDB(Base):
    __tablename__='Paper'

    id = Column(String, primary_key=True)
    name = Column(String)
    authors_ids = Column(list)
    date = Column(String)
    total_citations = Column(Integer)
