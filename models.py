import datetime
from flask_login import UserMixin
from __init__ import db, login_manager, bcrypt, app
from forms import BasketForm


@login_manager.user_loader
def load_user(user_id):
    return Customer.query.get(int(user_id))


class Employee(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False)


class Customer(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False)
    email = db.Column(db.String(length=100), nullable=False, unique=True)
    password_hash = db.Column(db.LargeBinary, nullable=False)

    @property
    def password(self):
        raise AttributeError("Plaintext password not stored")

    @password.setter
    def password(self, plaintext_password):
        self.password_hash = bcrypt.generate_password_hash(plaintext_password)

    def password_matches(self, plaintext_password):
        return bcrypt.check_password_hash(self.password_hash, plaintext_password)


class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=150), nullable=False, unique=True)
    quantity = db.Column(db.Integer(), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    department = db.Column(db.String(length=75), nullable=False)
    description = db.Column(db.String(length=1500), nullable=False)



    def __repr__(self):
        return f'Item {self.name}'





class Checkout(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    # cust_id = db.Column(db.Integer, db.ForeignKey(Customer.id))
    inputAddress1 = db.Column(db.String(length=50), nullable=False)
    inputAddress2 = db.Column(db.String(length=50), nullable=False)
    inputCity = db.Column(db.String(length=30), nullable=False)
    inputZip = db.Column(db.String(length=30), nullable=False)

with app.app_context():
    db.create_all()


class PAYMENTS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Account = db.Column(db.Integer)
    PaymentType = db.Column(db.String(20))
    Amount = db.Column(db.Integer)
    PaidBy = db.Column(db.String(60))
    DatePaid = db.Column(db.DateTime(), default=datetime.datetime.now())

    def __init__(self, Account, PaymentType, PaidBy):
        self.Account = Account
        self.PaymentType = PaymentType
        self.PaidBy = PaidBy

    def __repr__(self):
        return '<records %r>' % self.Account


class CustomerOrder(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    invoice = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.Integer, unique=False, nullable=False)
    customer_id = db.Column(db.Integer, unique=False, nullable=False)
    Date_created = db.Column(db.DateTime(), nullable=False, default=datetime.datetime.utcnow())

    def buy(self):
        form = BasketForm()
        if form.validate_on_submit:
            item_in_basket = CustomerOrder(id=Item.id, invoice=32, status='ordered', customer_id=1)
            Item.quantity -= 1
            db.session.add(item_in_basket)
            db.session.commit()
            return redirect(url_for('home_page'))

    def __repr__(self):
        return'<CustomerOrder %r>' % self.invoice



class ProductItem(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    descr = db.Column(db.Text,unique=True,nullable=True)
    price = db.Column(db.Float,nullable=False)
    cartitems = db.relationship('CartItem', backref='Product')
    def __repr__(self):
        return '<ProductName %r>' % self.name



# class CustomerOrder(db.model):
#     id = db.Column(db.Integer(),primary_key=True)
#     invoice = db.Column(db.String(20), unique=True, nullable=False)
#     status = db.Column(db.Integer, unique=False, nullable=False)
#     customer_id = db.Column(db.Integer, unique=False, nullable=False)
#     Date_created = db.Column(db.DateTime(), nullable=False, default=datetime.datetime.utcnow())
#
#     def __repr__(self):
#         return'<CustomerOrder %r>' % self.invoice
#
# db.create_all()

