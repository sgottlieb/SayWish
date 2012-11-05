from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm import relationship, backref

ENGINE = None
SESSION = None

Base = declarative_base()



class Wishlist(Base):
	__tablename__="wishlists"
	id = Column(Integer, primary_key = True)
	user_id = Column(Integer, nullable = True)
	item_id = Column(Integer, nullable = True)
	user = relationship("user", backref = backref("wishlists", order_by = id))

	def __init__(self, user_id, item_id):
		self.user_id = user_id
		self.item_id = item_id

class User(Base):
	__tablename__= "users"
	id = Column(Integer, primary_key = True)
	email = Column(String(64), nullable = True)
	password = Column(String(64), nullable = True)

	def __init__(self, email, password):
		self.email = email
		self.password = password

	@classmethod
	def new(cls, email, password):
		instance_row = cls(email, password)
		session.add(instance_row)
		session.commit()

class Item(Base):
	__tablename__ = "items"
	id = Column(Integer, primary_key = True)
	brand = Column(String(64), nullable=True)
	title = Column(String(64), nullable = True)
	size = Column(String(15), nullable = True)
	color = Column(String(20), nullable = True)
	price = Column(Integer, nullable = True)
	url = Column(String(300), nullable = True)
	image = Column(String(300), nullable = True)

	def __init__(self, brand, title, size, color, price, url, image):
		self.brand = brand
		self.title = title
		self.size = size
		self.color = color
		self.price = price
		self.url = url
		self.image = image



def connect():
    global ENGINE
    global Session 
    ENGINE = create_engine("sqlite:///wishlists.db", echo=True)
    Session = sessionmaker(bind=ENGINE)
    Base.metadata.create_all(ENGINE)
    return Session()
