from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import *
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin@localhost/FemInstant'
app.config['SECRET_KEY'] = 'ebd0469c4b70bf520c31c39a'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


class Employee(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    location = db.Column(db.String(length=50), nullable=False)
    # customers = db.relationship('Customer', backref='delivery_driver', lazy=True)


class Customer(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_name = db.Column(db.String(length=15), nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)
    customer_name = db.Column(db.String(length=30), nullable=False)
    customer_email = db.Column(db.String(length=100), nullable=False)
    location = db.Column(db.String(length=50), nullable=False)
    # items = db.relationship('Item', backref='owned_user', lazy=True)
    # delivery_driver_id = db.Column(db.Integer(), db.ForeignKey(Employee.id))

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')


class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=150), nullable=False, unique=True)
    quantity = db.Column(db.Integer(), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    department = db.Column(db.String(length=75), nullable=False)
    description = db.Column(db.String(length=1500), nullable=False)
    # owner = db.Column(db.Integer(), db.ForeignKey(Customer.id))

    def __repr__(self):
        return f'Item {self.name}'


with app.app_context():
    db.create_all()


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('index.html')


@app.route('/')
@app.route('/login')
def login_page():
    return render_template('login.html')

# @app.route('/register')
# def register():
#     form = RegisterForm()
#     return render_template('register.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = Customer(customer_name=form.customer_name,
                                  user_name=form.user_name.data,
                                  email=form.customer_email.data,
                                  password_hash=form.password.data)

        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('home_page'))
    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

        # flash(f'Account created successfully for {form.username.data}', category='success')
        return redirect(url_for('login_page'))
    return render_template('register.html', title='Register', form=form)

@app.route('/')
@app.route('/checkout')
def checkout_page():
    return render_template('checkout.html')
#
#
# @app.route('/products')
# def products_page():
#     items = [
#         {'productID': 1, 'item_name': 'Cerave Hydrating Cleanser with Hyaluronic Acid', 'quantity': '50',
#          'price': '9.99', 'Location': 'North London'},
#         {'productID': 2, 'item_name': 'Simple Kind To Skin Cleansing Wipes Biodegradable X50', 'quantity': '50',
#          'price': '9.99', 'Location': 'North London'},
#         {'productID': 3, 'item_name': 'Simple Kind to Skin Refreshing Facial Wash Gel 50ml', 'quantity': '50',
#          'price': '9.99', 'Location': 'North London'},
#         {'productID': 4, 'item_name': 'CeraVe Moisturising Lotion For Dry to Very Dry Skin 236ml', 'quantity': '50',
#          'price': '9.99', 'Location': 'North London'},
#         {'productID': 5, 'item_name': "Burt's Bees® Beeswax Lip Balm 4.25g", 'quantity': '50', 'price': '9.99',
#          'Location': 'North London'},
#         {'productID': 6, 'item_name': "NYX Professional Makeup Setting Spray Matte", 'quantity': '50', 'price': '9.99',
#          'Location': 'North London'},
#         {'productID': 7, 'item_name': "NYX Professional Makeup Micro Brow Pencil (Various Shades)", 'quantity': '50',
#          'price': '9.99',
#          'Location': 'North London'},
#         {'productID': 8, 'item_name': "NYX Professional Makeup Butter Gloss - Praline", 'quantity': '50',
#          'price': '9.99', 'Location': 'North London'},
#         {'productID': 9, 'item_name': "Maybelline Lash Sensational Sky High Mascara 01 Black", 'quantity': '50',
#          'price': '9.99', 'Location': 'North London'},
#         {'productID': 10, 'item_name': "NYX Professional Makeup Suede Matte Lip Liner (Various Shades)",
#          'quantity': '50', 'price': '9.99', 'Location': 'North London'},
#         {'productID': 11, 'item_name': "Always Maxi Long Plus Sanitary Towels x12", 'quantity': '50', 'price': '9.99',
#          'Location': 'North London'},
#         {'productID': 12, 'item_name': "Always Ultra Secure Night Duo Sanitary Towels Multipack 18", 'quantity': '50',
#          'price': '9.99', 'Location': 'North London'},
#         {'productID': 13, 'item_name': "Always Sensitive Normal Ultra (Size 1) Sanitary Towels x16", 'quantity': '50',
#          'price': '9.99', 'Location': 'North London'},
#         {'productID': 14, 'item_name': "Tampax Compak Regular Tampons 18", 'quantity': '50', 'price': '9.99',
#          'Location': 'North London'},
#         {'productID': 15, 'item_name': "OrganiCup, Size A, Menstrual Cup, 1 unit", 'quantity': '50', 'price': '9.99',
#          'Location': 'North London'},
#         {'productID': 16, 'item_name': "Bodyform So Slim Pantyliners 34 Pack", 'quantity': '50', 'price': '9.99',
#          'Location': 'North London'},
#         {'productID': 17, 'item_name': "Tampax Compak Lite Applicator Tampon Single 18PK", 'quantity': '50',
#          'price': '9.99', 'Location': 'North London'},
#
#     ]
#     return render_template('products.html', items=items)


if __name__ == '__main__':
    app.run(port=5006, debug=True)