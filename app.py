from re import L
import re
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
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
    lead_time_days = db.Column(db.Integer)
    recurrence_purchase_days = db.Column(db.Integer)
    # many-to-one scalar
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.supplier_id'))
    supplier = db.relationship("Supplier", back_populates="products")
    #many to many (deals)
    deals = db.relationship("Deal", secondary=association_table, back_populates="products")

    def __init__(self, product_name, description, target_price, lead_time_days, recurrence_purchase_days, supplier_id):
        self.product_name = product_name
        self.description = description
        self.target_price = target_price
        self.lead_time_days = lead_time_days
        self.recurrence_purchase_days = recurrence_purchase_days
        self.supplier_id = supplier_id

    def __repr__(self):
        return "<product_id {}>".format(self.product_id)

    def serialize(self):
        return {
            "product_id": self.product_id, 
            "product_name": self.product_name, 
            "description":self.description,
            "target_price":self.target_price,
            "lead_time_days":self.lead_time_days,
            "recurrence_purchase_days":self.recurrence_purchase_days,
            "supplier_id":self.supplier_id

        }


class Buyer(db.Model):
    __tablename__ = "buyer"
    buyer_id = db.Column(db.Integer, primary_key=True)
    buyer_name = db.Column(db.String(50))
    #one to many
    deals = db.relationship("Deal", back_populates="buyer")

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

# API
###########################################################
# DEAL
###########################################################
@app.route("/deals")
def get_all_deals():
    try:
        deals = Deal.query.all()
        return jsonify([e.serialize() for e in deals])
    except Exception as e:
        return str(e)

@app.route("/in_process")
def get_all_deals_in_process():
    try:
        deals = Deal.query.filter_by(
        status="In proccess")
        return jsonify([e.serialize() for e in deals])
    except Exception as e:
        return str(e)

@app.route("/success")
def get_all_deals_success():
    try:
        deals = Deal.query.filter_by(
        status="Success")
        return jsonify([e.serialize() for e in deals])
    except Exception as e:
        return str(e)

@app.route("/failure")
def get_all_deals_failure():
    try:
        deals = Deal.query.filter_by(
        status="Failure")
        return jsonify([e.serialize() for e in deals])
    except Exception as e:
        return str(e)

@app.route("/deals/<string:deal_id>")
def get_one_deal_by_id(deal_id):
    deal = Deal.query.get_or_404(deal_id)
    return deal.serialize()

@app.route("/deals", methods=["POST"])
def create_deal():
    if "status" not in request.json:
        return {"error": "Deal status is missing"}, 412
    if "buyer_id" not in request.json:
        return {"error": "Deal buyer id is missing"}, 412

    status = request.json["status"]
    buyer_id = request.json["buyer_id"]

    try:
        deal = Deal(
            status=status,
            buyer_id=buyer_id
        )
        db.session.add(deal)
        db.session.commit()
        return "Deal added. Deal id={}".format(deal.deal_id)
    except Exception as e:
        return str(e)

@app.route("/deals/<string:deal_id>", methods=["PUT"])
def update_deal(deal_id):
    deal = Deal.query.get_or_404(deal_id)
    if 'status' in request.json:
        deal.status = request.json['status']
    db.session.commit()
    return deal.serialize()

@app.route("/deals/<string:deal_id>", methods=['DELETE'])
def delete_deal(deal_id):
    deal = Deal.query.get_or_404(deal_id)
    db.session.delete(deal)
    db.session.commit()
    return "Deal deleted"

###########################################################
# PRODUCT
###########################################################
@app.route("/products")
def get_all_products():
    try:
        products = Product.query.all()
        return jsonify([e.serialize() for e in products])
    except Exception as e:
        return str(e)

@app.route("/products/<string:product_id>")
def get_one_product_by_id(product_id):
    product = Product.query.get_or_404(product_id)
    return product.serialize()

@app.route("/products", methods=["POST"])
def create_product():
    if "product_name" not in request.json:
        return {"error": "Product name is missing"}, 412
    if "description" not in request.json:
        return {"error": "Product description is missing"}, 412
    if "target_price" not in request.json:
        return {"error": "Product target price is missing"}, 412
    if "lead_time_days" not in request.json:
        return {"error": "Product lead time in days is missing"}, 412
    if "recurrence_purchase_days" not in request.json:
        return {"error": "Product recurrence purchase in days is missing"}, 412
    if "supplier_id" not in request.json:
        return {"error": "Product supplier id is missing"}, 412

    product_name = request.json["product_name"]
    description = request.json["description"]
    target_price = request.json["target_price"]
    lead_time_days = request.json["lead_time_days"]
    recurrence_purchase_days = request.json["recurrence_purchase_days"]
    supplier_id = request.json["supplier_id"]

    try:
        product = Product(
            product_name = product_name,
            description = description,
            target_price = target_price,
            lead_time_days = lead_time_days,
            recurrence_purchase_days = recurrence_purchase_days,
            supplier_id = supplier_id
        )
        db.session.add(product)
        db.session.commit()
        return "Product added. Product id={}".format(product.product_id)
    except Exception as e:
        return str(e)

@app.route("/products/<string:product_id>", methods=["PUT"])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    if 'product_name' in request.json:
        product.product_name = request.json['product_name']
    if 'description' in request.json:
        product.description = request.json['description']
    if 'target_price' in request.json:
        product.target_price = request.json['target_price']
    if 'lead_time_days' in request.json:
        product.lead_time_days = request.json['lead_time_days']
    if 'recurrence_purchase_days' in request.json:
        product.recurrence_purchase_days = request.json['recurrence_purchase_days']
    if 'supplier_id' in request.json:
        product.supplier_id = request.json['supplier_id']
    db.session.commit()
    return product.serialize()

@app.route("/products/<string:product_id>", methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return "Product deleted"

###########################################################
# BUYER
###########################################################
@app.route("/buyers")
def get_all_buyers():
    try:
        buyers = Buyer.query.all()
        return jsonify([e.serialize() for e in buyers])
    except Exception as e:
        return str(e)

@app.route("/buyers/<string:buyer_id>")
def get_one_buyer_by_id(buyer_id):
    buyer = Buyer.query.get_or_404(buyer_id)
    return buyer.serialize()

@app.route("/buyers", methods=["POST"])
def create_buyer():
    if "buyer_name" not in request.json:
        return {"error": "Buyer name is missing"}, 412

    buyer_name = request.json["buyer_name"]
    
    try:
        buyer = Buyer(
            buyer_name=buyer_name
        )
        db.session.add(buyer)
        db.session.commit()
        return "Buyer added. Buyer id={}".format(buyer.buyer_id)
    except Exception as e:
        return str(e)

@app.route("/buyers/<string:buyer_id>", methods=["PUT"])
def update_buyer(buyer_id):
    buyer = Buyer.query.get_or_404(buyer_id)
    if 'buyer_name' in request.json:
        buyer.buyer_name = request.json['buyer_name']
    db.session.commit()
    return buyer.serialize()

@app.route("/buyers/<string:buyer_id>", methods=['DELETE'])
def delete_buyer(buyer_id):
    buyer = Buyer.query.get_or_404(buyer_id)
    db.session.delete(buyer)
    db.session.commit()
    return "Buyer deleted"

###########################################################
# SUPPLIER
###########################################################
@app.route("/suppliers")
def get_all_suppliers():
    try:
        suppliers = Supplier.query.all()
        return jsonify([e.serialize() for e in suppliers])
    except Exception as e:
        return str(e)

@app.route("/suppliers/<string:supplier_id>")
def get_one_supplier_by_id(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    return supplier.serialize()

@app.route("/suppliers", methods=["POST"])
def create_supplier():
    if "supplier_name" not in request.json:
        return {"error": "Supplier name is missing"}, 412

    supplier_name = request.json["supplier_name"]
    
    try:
        supplier = Supplier(
            supplier_name=supplier_name
        )
        db.session.add(supplier)
        db.session.commit()
        return "Supplier added. Supplier id={}".format(supplier.supplier_id)
    except Exception as e:
        return str(e)

@app.route("/suppliers/<string:supplier_id>", methods=["PUT"])
def update_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    if 'supplier_name' in request.json:
        supplier.supplier_name = request.json['supplier_name']
    db.session.commit()
    return supplier.serialize()

@app.route("/suppliers/<string:supplier_id>", methods=['DELETE'])
def delete_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    db.session.delete(supplier)
    db.session.commit()
    return "Supplier deleted"
 
if __name__ == "__main__":
    app.run(debug=True)