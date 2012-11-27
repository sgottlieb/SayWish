from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm import relationship, backref
from bs4 import BeautifulSoup
import datetime

# ENGINE = None
# SESSION = None

# Base = declarative_base()

today = datetime.datetime.now()

engine = create_engine("sqlite:///wishlists.db", echo=False)
SESSION = scoped_session(sessionmaker(bind= engine, autocommit= False, autoflush = False))

Base = declarative_base()
Base.query = SESSION.query_property()

class Wishlist(Base):
	__tablename__="wishlists"
	id = Column(Integer, primary_key = True)
	user_id = Column(Integer, ForeignKey('users.id'), nullable = True)
	item_id = Column(Integer,  ForeignKey('items.id'),nullable = True)
	user = relationship("User", backref = backref("wishlists", order_by = id))
	item = relationship("Item", backref = backref("wishlists", order_by = id))

	def __init__(self, user_id, item_id):
		self.user_id = user_id
		self.item_id = item_id

	@classmethod
	def new(cls, user_id, item_id):
		instance_row = cls(user_id, item_id)
		SESSION.add(instance_row)
		SESSION.commit()

	@classmethod
	def search(cls, input_user_id):
		wishlist_list = SESSION.query(cls).filter_by(user_id= input_user_id).all()
		return wishlist_list

	@classmethod
	def search_groups(cls, input_user_id):
		group_list =[]
		wishlist_list = Wishlist.search(input_user_id)
		for items in wishlist_list:
			if items.item.title not in group_list:
				group_list.append(items.item.title)
		return group_list

	@classmethod
	def delete(cls, input_item):
		SESSION.query(cls).filter_by(item_id= input_item).delete()


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
		SESSION.add(instance_row)
		SESSION.commit()
		
	@classmethod
	def authenticate(cls, input_email, input_password):
		user = SESSION.query(User).filter_by(email= input_email).first()
		if user and input_password == user.password:
			return user      
		return None

class Item(Base):
	__tablename__ = "items"
	id = Column(Integer, primary_key = True)
	brand = Column(String(64), nullable=True)
	title = Column(String(64), nullable = True)
	price = Column(String(10), nullable = True)
	url = Column(String(1000),nullable = True)
	host_url = Column(String(100), nullable = True)
	timestamp = Column(DateTime, nullable = True)
	image = Column(String(300), nullable = True)
	
	def __init__(self, brand, title, price, url, host_url,timestamp, image):
		self.brand = brand
		self.title = title
		self.price = price
		self.url = url
		self.host_url = host_url
		self.timestamp = timestamp
		self.image = image

	@classmethod
	def new(cls, brand, title, price, url, host_url, image):
		timestamp = datetime.datetime.now()
		instance_row = cls(brand, title, price, url, host_url, timestamp, image)
		SESSION.add(instance_row)
		SESSION.commit()
		return instance_row.id

	@classmethod
	def search(cls, input_item_id):
		item = SESSION.query(cls).filter_by(id= input_item_id).first()
		return item

	@classmethod
	def delete(cls, input_item_id):
		SESSION.query(Item).filter_by(id=input_item_id).delete()
		Wishlist.delete(input_item_id)
		SESSION.commit()
		return 

class Website(Base):
	__tablename__="websites"
	id = Column(Integer, primary_key=True)
	hostname = Column(String(100), nullable = True)
	price_class = Column(String(64), nullable = True)
	brand_class = Column(String(64), nullable = True)
	image_path = Column(String(300), nullable = True)

	def __init__(self, hostname, price_class, brand_class, image_path):
		self.hostname = hostname
		self.price_class = price_class
		self.brand_class = brand_class
		self.image_path = image_path

	@classmethod
	def new(cls, hostname, price_class, brand_class, image_path):
		instance_row = cls(hostname, price_class, brand_class, image_path)
		SESSION.add(instance_row)
		SESSION.commit()

	@classmethod
	def search(cls, input_hostname):
		website = SESSION.query(Website).filter_by(hostname= input_hostname).first()
		if website:
			return website
		else:
			return None

def connect():
	global ENGINE
	global Session 
	ENGINE = create_engine("sqlite:///wishlists.db", echo=True)
	Session = sessionmaker(bind=ENGINE)
	Base.metadata.create_all(ENGINE)
	return Session()
