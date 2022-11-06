from flask import flash, redirect, url_for, request, session
from flask_login import login_user, logout_user
from forms import RegisterForm, LoginForm, CheckoutForm
from __init__ import app, db, login_manager
from ex import stripe_keys
from basket import initialise_basket, render_template_with_basket_quantity, get_items_from_basket, increase_item_quantity_in_basket, decrease_item_quantity_in_basket, get_basket_total
from models import Item, Customer


@login_manager.user_loader
def load_user(user_id):
    return Customer.query.get(int(user_id))


@app.route('/')
@app.route('/home')
@initialise_basket
def home_page():
    return render_template_with_basket_quantity('index.html')


@app.route('/login', methods=['GET', 'POST'])
@initialise_basket
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        matching_user = Customer.query.filter_by(email=form.email.data).first()
        if matching_user and matching_user.password_matches(form.password.data):
            login_user(matching_user)
            flash('Success! You have logged in', category='success')
            return redirect(url_for('home_page'))
        else:
            flash('Username and Password do not match', category='danger')
    return render_template_with_basket_quantity('login.html', title='Log in', form=form)


@app.route('/register', methods=['GET', 'POST'])
@initialise_basket
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_with_same_email = Customer.query.filter_by(email=form.email.data).first()
        if user_with_same_email:
            flash('An account with that email already exists', category='danger')
        else:
            user_to_create = Customer(name=form.name.data, email=form.email.data, password=form.password.data)
            db.session.add(user_to_create)
            db.session.commit()
            login_user(user_to_create)
            flash(f'Account created successfully for {form.name.data}', category='success')
            return redirect(url_for('profile_page'))
    return render_template_with_basket_quantity('register.html', title='Register', form=form)


@app.route('/products')
@initialise_basket
def products_page():
    department = request.args.get('department')
    items = db.session.query(Item)
    if department in ['Skincare', 'Makeup', 'Feminine Hygiene']:
        items = items.filter_by(department=department)
    return render_template_with_basket_quantity('products.html', items=items, department=department)


@app.route('/increase_quantity/<item_id>', methods=['POST'])
def increase_quantity_in_basket(item_id):
    increase_item_quantity_in_basket(item_id)
    if request.form.get('referrer').startswith(url_for('products_page')):
        flash('Item added to basket', 'success')
    return redirect(request.form.get('referrer'))


@app.route('/decrease_quantity/<item_id>', methods=['POST'])
def decrease_quantity_in_basket(item_id):
    decrease_item_quantity_in_basket(item_id)
    return redirect(request.form.get('referrer'))


# TODO
@app.route('/basket')
@initialise_basket
def basket_page():
    items = get_items_from_basket()
    basket_total = get_basket_total()
    return render_template_with_basket_quantity('basket.html', items=items, basket_total=basket_total)


# TODO
@app.route('/checkout', methods=['GET', 'POST'])
@initialise_basket
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
    return render_template_with_basket_quantity('checkout.html', title='Checkout', form=form)


# TODO
@app.route('/payment')
@initialise_basket
def payment_page():
    return render_template_with_basket_quantity('payment.html')


@app.route('/logout', methods=['POST'])
def logout_page():
    logout_user()
    flash('You have logged out successfully', category='success')
    return redirect(url_for('home_page'))


# @app.route('/map')
# def map_func():
#     return render_template('map.html', apikey=api_key, latitude=latitude, longitude=longitude, address=address)


@app.route('/pay')
@initialise_basket
def pay():
    return render_template_with_basket_quantity('checkout1.html', key=stripe_keys['publishable_key'])


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

    return render_template_with_basket_quantity('charge.html', amount=amount)


if __name__ == '__main__':
    app.run(port=5006, debug=True)
