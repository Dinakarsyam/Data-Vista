from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

Base = declarative_base()

class Store(Base):
    __tablename__ = 'stores'
    storeid = Column(Integer, primary_key=True)
    storelocation = Column(String)
    orders = relationship("Order", back_populates="store")

class Product(Base):
    __tablename__ = 'products'
    productid = Column(Integer, primary_key=True)
    productname = Column(String)
    category = Column(String)
    subcategory = Column(String)
    orders = relationship("Order", back_populates="product")

class SalesTeam(Base):
    __tablename__ = 'salesteam'
    salespersonid = Column(Integer, primary_key=True)
    salespersonname = Column(String)
    orders = relationship("Order", back_populates="salesperson")

class Order(Base):
    __tablename__ = 'orders'
    orderid = Column(Integer, primary_key=True)
    orderdate = Column(Date)
    storeid = Column(Integer, ForeignKey('stores.storeid'))
    productid = Column(Integer, ForeignKey('products.productid'))
    salespersonid = Column(Integer, ForeignKey('salesteam.salespersonid'))
    orderstatus = Column(String)
    profit = Column(Float)
    quantity = Column(Integer)
    costofgoodssold = Column(Float)
    paymentmethod = Column(String)
    totalprice = Column(Float)
    shippingcost = Column(Float)
    discount = Column(Float)
    customerfeedback = Column(String)
    deliverydate = Column(Date)
    unitprice = Column(Float)

    store = relationship("Store", back_populates="orders")
    product = relationship("Product", back_populates="orders")
    salesperson = relationship("SalesTeam", back_populates="orders")

engine = create_engine(DATABASE_URI)
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
