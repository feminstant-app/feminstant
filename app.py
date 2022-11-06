from flask import Flask, render_template, flash, redirect, url_for, request
from forms import RegisterForm, LoginForm, CheckoutForm, BasketForm
from flask_login import login_user, logout_user, login_required
from ex import stripe_keys
from models import *
from __init__ import app
import datetime


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
# @login_required
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


@app.route('/hygiene', methods=['GET', 'POST'])
def hygiene_products_page():
    basket_form = BasketForm()
    Buy()
    items = db.session.query(Item).filter(Item.department == "Feminine Hygiene")
    return render_template('Hygiene.html', items=items, basket_form=basket_form)


@app.route('/makeup', methods=['GET', 'POST'])
def makeup_products_page():
    basket_form = BasketForm()
    items = db.session.query(Item).filter(Item.department == "Makeup")
    return render_template('makeup.html', items=items, basket_form=basket_form)


@app.route('/skincare', methods=['GET', 'POST'])
def skincare_products_page():
    basket_form = BasketForm()
    items = db.session.query(Item).filter(Item.department == "Skincare")
    return render_template('skincare.html', items=items, basket_form=basket_form)


@app.route('/payment')
def payment_page():
    return render_template('payment.html')


@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have logged out successfully', category='info')
    return redirect(url_for('home_page'))


@app.route('/map')
def map_func():
    return render_template('map.html', apikey=api_key, latitude=latitude, longitude=longitude, address=address)


@app.route('/pay')
def pay():
    return render_template('checkout1.html', key=stripe_keys['publishable_key'])


@app.route('/charge', methods=['POST'])
def charge():
    # Amount in cents
    amount = 500

    customer = stripe.Customer.create(
        email='customer@example.com',
        source=request.form['stripeToken']
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Flask Charge'
    )

    return render_template('charge.html', amount=amount)


if __name__ == '__main__':
    app.run(port=5006, debug=True)
