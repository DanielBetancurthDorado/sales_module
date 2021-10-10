from re import L
import re
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)
# Models
#association table
association_table = db.Table('deals-products',
    db.Column('deal_id', db.ForeignKey('deal.deal_id'), primary_key=True),
    db.Column('product_id', db.ForeignKey('product.product_id'), primary_key=True)
)
class Deal(db.Model):
    #atts
    __tablename__ = "deal"
    deal_id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20))
    # many-to-one scalar
    buyer_id = db.Column(db.Integer, db.ForeignKey('buyer.buyer_id'))
    buyer = db.relationship("Buyer", back_populates="deals")
    #many to many (products)
    products = db.relationship("Product",secondary=association_table,back_populates="deals")

    def __init__(self, status, buyer_id):
        self.status = status
        self.buyer_id = buyer_id

    def __repr__(self):
        return "<deal_id {}>".format(self.deal_id)

    def serialize(self):
        return {
            "deal_id": self.deal_id,
            "status": self.status,
            "buyer_id" : self.buyer_id
        }


class Product(db.Model):
    __tablename__ = "product"
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100))
    description = db.Column(db.String(250))
    target_price = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    lead_time_days = db.Column(db.Integer)
    recurrence_purchase_days = db.Column(db.Integer)
    # many-to-one scalar
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.supplier_id'))
    supplier = db.relationship("Supplier", back_populates="products")
    #one to many
    comments = db.relationship("Comment", back_populates="product")
    #many to many (deals)
    deals = db.relationship("Deal", secondary=association_table, back_populates="products")

    def __init__(self, product_name, description, target_price, quantity, lead_time_days, recurrence_purchase_days):
        self.product_name = product_name
        self.description = description
        self.target_price = target_price
        self.quantity = quantity
        self.lead_time_days = lead_time_days
        self.recurrence_purchase_days = recurrence_purchase_days

    def __repr__(self):
        return "<product_id {}>".format(self.product_id)

    def serialize(self):
        return {
            "product_id": self.product_id, 
            "product_name": self.product_name, 
            "description":self.description,
            "target_price":self.target_price,
            "quantity":self.quantity,
            "lead_time_days":self.lead_time_days,
            "recurrence_purchase_days":self.recurrence_purchase_days,

        }


class Buyer(db.Model):
    __tablename__ = "buyer"
    buyer_id = db.Column(db.Integer, primary_key=True)
    buyer_name = db.Column(db.String(50))
    #one to many
    deals = db.relationship("Deal", back_populates="buyer")
    #one to one
    comment = db.relationship("Comment", back_populates="buyer", uselist=False)

    def __init__(self, buyer_name):
        self.buyer_name = buyer_name

    def __repr__(self):
        return "<buyer_id {}>".format(self.buyer_id)

    def serialize(self):
        return {
            "buyer_id": self.buyer_id,
            "buyer_name": self.buyer_name,
        }

class Supplier(db.Model):
    __tablename__ = "supplier"
    supplier_id = db.Column(db.Integer, primary_key=True)
    supplier_name = db.Column(db.String(50))
    #one to many
    products = db.relationship("Product", back_populates="supplier")

    def __init__(self, supplier_name):
        self.supplier_name = supplier_name

    def __repr__(self):
        return "<supplier_id {}>".format(self.supplier_id)

    def serialize(self):
        return {
            "supplier_id": self.supplier_id,
            "supplier_name": self.supplier_name,
        }

class Comment(db.Model):
    __tablename__ = "comment"
    comment_id = db.Column(db.Integer, primary_key=True)
    comment_message = db.Column(db.String(500))
    # one-to-one
    buyer_id = db.Column(db.Integer, db.ForeignKey('buyer.buyer_id'))
    buyer = db.relationship("Buyer", back_populates="comment")
    #many to one
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'))
    product = db.relationship("Product", back_populates="comments")

    def __init__(self, comment_message):
        self.comment_message = comment_message

    def __repr__(self):
        return "<comment_id {}>".format(self.comment_id)

    def serialize(self):
        return {
            "comment_id": self.comment_id,
            "comment_message": self.comment_message,
        }

if __name__ == "__main__":
    app.run(debug=True)