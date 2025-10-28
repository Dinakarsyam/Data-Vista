from apps import db

class Store(db.Model):
    __tablename__ = 'stores'
    storeid = db.Column(db.Integer, primary_key=True)
    storelocation = db.Column(db.String)
    orders = db.relationship("Order", back_populates="store")

class Product(db.Model):
    __tablename__ = 'products'
    productid = db.Column(db.Integer, primary_key=True)
    productname = db.Column(db.String)
    category = db.Column(db.String)
    subcategory = db.Column(db.String)
    orders = db.relationship("Order", back_populates="product")

class SalesTeam(db.Model):
    __tablename__ = 'salesteam'
    salespersonid = db.Column(db.Integer, primary_key=True)
    salespersonname = db.Column(db.String)
    orders = db.relationship("Order", back_populates="salesperson")

class Order(db.Model):
    __tablename__ = 'orders'
    orderid = db.Column(db.Integer, primary_key=True)
    orderdate = db.Column(db.Date)
    storeid = db.Column(db.Integer, db.ForeignKey('stores.storeid'))
    productid = db.Column(db.Integer, db.ForeignKey('products.productid'))
    salespersonid = db.Column(db.Integer, db.ForeignKey('salesteam.salespersonid'))
    orderstatus = db.Column(db.String)
    profit = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    costofgoodssold = db.Column(db.Float)
    paymentmethod = db.Column(db.String)
    totalprice = db.Column(db.Float)
    shippingcost = db.Column(db.Float)
    discount = db.Column(db.Float)
    customerfeedback = db.Column(db.String)
    deliverydate = db.Column(db.Date)
    unitprice = db.Column(db.Float)

    store = db.relationship("Store", back_populates="orders")
    product = db.relationship("Product", back_populates="orders")
    salesperson = db.relationship("SalesTeam", back_populates="orders")
