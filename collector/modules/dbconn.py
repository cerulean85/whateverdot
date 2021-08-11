import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

engine = sqlalchemy.create_engine("mariadb+mariadbconnector://tester:123456@localhost:3306/whateverdot")
Base = declarative_base()


class Test(Base):
    __tablename__ = "test"
    d1 = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    d2 = sqlalchemy.Column(sqlalchemy.Float)
    d3 = sqlalchemy.Column(sqlalchemy.String(length=100))
    d4 = sqlalchemy.Column(sqlalchemy.DateTime)

Session = sqlalchemy.orm.sessionmaker()
Session.configure(bind=engine)
session = Session()

test_list = session.query(Test).all()
for test in test_list:
    print("{} {} {}".format(test.d1, test.d2, test.d3, test.d4))


# https://mariadb.com/ko/resources/blog/using-sqlalchemy-with-mariadb-connector-python-part-1/
