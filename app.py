from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import RegisterForm, LoginForm, CheckoutForm
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, UserMixin, logout_user, login_required


app = Flask(__name__)
app.config['SECRET_KEY'] = 'ebd0469c4b70bf520c31c39a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin@localhost/FemInstant'
db = SQLAlchemy(app)
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)


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

    # def password_matches(self, plaintext_password):
    #     return self.password_hash == str.encode(plaintext_password)


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
            login_user(matching_user)
            flash('Success! You have logged in', category='success')
            return redirect(url_for('makeup_products_page'))
        else:
            flash('Username and Password do not match', category='danger')
    return render_template('login.html', title='Log in', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = Customer(name=form.name.data, email=form.email.data, password=form.password.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account created successfully for {form.name.data}', category='success')
        return redirect(url_for('profile_page'))
    return render_template('register.html', title='Register', form=form)


@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout_page():
    form = CheckoutForm()
    if form.validate_on_submit():
        checkout_information = Checkout(inputAddress1=form.inputAddress1.data,
                                        inputAddress2=form.inputAddress2.data, inputCity=form.inputCity.data,
                                        inputZip=form.inputZip.data)
        db.session.add(checkout_information)
        db.session.commit()
        flash("Checkout complete", category='success')
        return redirect(url_for('home_page'))
    return render_template('checkout.html', title='Checkout', form=form)


@app.route('/profile')
def profile_page():
    return render_template('profile.html')


@app.route('/hygiene')
def hygiene_products_page():
    items = db.session.query(Item).filter(Item.department == "Feminine Hygiene")
    # print(items)
    return render_template('Hygiene.html', items=items)


@app.route('/makeup')
def makeup_products_page():
    items = db.session.query(Item).filter(Item.department == "Makeup")
    # print(items)
    return render_template('Makeup.html', items=items)


@app.route('/skincare')
def skincare_products_page():
    items = db.session.query(Item).filter(Item.department == "Skincare")
    # print(items)
    return render_template('skincare.html', items=items)


@app.route('/payment')
def payment_page():
    return render_template('payment.html')


@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have logged out successfully', category='info')
    return redirect(url_for('home_page'))


if __name__ == '__main__':
    app.run(port=5006, debug=True)
