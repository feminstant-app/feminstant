from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import RegisterForm, LoginForm
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SECRET_KEY'] = 'ebd0469c4b70bf520c31c39a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin@localhost/FemInstant'
db = SQLAlchemy(app)
db.init_app(app)
bcrypt = Bcrypt(app)


class Employee(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False)


class Customer(db.Model):
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


with app.app_context():
    db.create_all()


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        matching_user = Customer.query.filter_by(email=form.email.data).first()
        if matching_user and matching_user.password_matches(form.password.data):
            print("Success!")
            return redirect(url_for('home_page'))
    return render_template('login.html', title='Log in', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = Customer(name=form.name.data, email=form.email.data)
        user_to_create.password = form.password.data
        db.session.add(user_to_create)
        db.session.commit()
        flash(f'Account created successfully for {form.name.data}', category='success')
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