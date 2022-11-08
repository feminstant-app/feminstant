from flask_login import UserMixin
from base import app, db, bcrypt


class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=150), nullable=False, unique=True)
    quantity = db.Column(db.Integer(), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    department = db.Column(db.String(length=75), nullable=False)
    description = db.Column(db.String(length=1500), nullable=False)

    def __hash__(self):
        return hash(self.id)


class Customer(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False)
    email = db.Column(db.String(length=100), nullable=False, unique=True)
    password_hash = db.Column(db.LargeBinary, nullable=False)
    orders = db.relationship('Order', backref='customer')

    @property
    def password(self):
        raise AttributeError("Plaintext password not stored")

    @password.setter
    def password(self, plaintext_password):
        self.password_hash = bcrypt.generate_password_hash(plaintext_password)

    def password_matches(self, plaintext_password):
        return bcrypt.check_password_hash(self.password_hash, plaintext_password)


order_items = db.Table('order_items',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('item_id', db.Integer, db.ForeignKey('item.id'), primary_key=True),
    db.Column('quantity', db.Integer, nullable=False)
)


class Order(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(Customer.id), nullable=True)
    date = db.Column(db.Date(), nullable=False)
    house = db.Column(db.String(length=50), nullable=False)
    street = db.Column(db.String(length=50), nullable=False)
    city = db.Column(db.String(length=30), nullable=False)
    postcode = db.Column(db.String(length=8), nullable=False)
    items = db.relationship('Item', secondary=order_items, backref=db.backref('orders'))


with app.app_context():
    db.create_all()
