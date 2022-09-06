from venv import create
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

engine = create_engine("mysql+pymysql://root:estuate@localhost:3300/pets", echo=True)
conn = engine.connect()
# print(conn)

"""
class User:
    id : int
    username : str
    email : str

class Post:
    id : int
    title : str
    content : str
    user_id : int
"""

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True)
    username = Column(String(30), nullable = False, unique = True)
    email = Column(String(30), nullable = True)
    posts = relationship("Post", backref="author")

    def __repr__(self) -> str:
        return f"<User {self.username}>"

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key = True)
    title = Column(String(300), nullable=False)
    content = Column(String(3000), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    def __repr__(self) -> str:
        return f"<Post {self.user_id}, {self.title}>"
    
Base.metadata.create_all(engine)

user = User(username="shyamsundar", email="nrshyamsundariyanger@gmail.com")
Session = sessionmaker(engine)
db = Session()

db.add(user)
db.commit()

# in a one to many relation the ORM Model goes as follows 
# the children contains the ForeignKey attribute which is referenced to parent's column
# the parent contains the member variable relationship which contains the list of possible values.
# relationship syntax : relationship("<child class name>")
# * if the child is supposed to have many to one relationship backwards we need to mention 
#   the relationship.back_populates attribute
# * alternatively the relationship.backref attribute can also be used to do the same.

# in many to one relation the ORM model goes as follows
# the parent contains the ForeignKey attribute which is followed by children's column
# children contains the relationship attribute