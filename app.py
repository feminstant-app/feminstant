from flask import flash, redirect, url_for, request, session
from flask_login import login_user, logout_user, current_user
from utils.forms import RegisterForm, LoginForm, CheckoutForm
from datetime import date

from base import app, db, login_manager, postcode_manager
from utils.basket import initialise_basket, render_template_with_basket_quantity, get_items_from_basket, \
    increase_item_quantity_in_basket, decrease_item_quantity_in_basket, get_basket_total
from utils.models import Item, Customer, Order, order_items
from config import STRIPE_PUBLISHABLE_KEY


@login_manager.user_loader
def load_user(user_id):
    return Customer.query.get(int(user_id))


@app.route('/')
@app.route('/home')
@initialise_basket
def home_page():
    return render_template_with_basket_quantity('index.html')


@app.route('/about')
@initialise_basket
def about_page():
    return render_template_with_basket_quantity('about.html')


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
    basket = session['basket']
    if department in ['Skincare', 'Makeup', 'Feminine Hygiene']:
        items = items.filter_by(department=department)
    return render_template_with_basket_quantity('products.html', department=department, items=items, basket=basket)


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


@app.route('/basket')
@initialise_basket
def basket_page():
    items = get_items_from_basket(session['basket'])
    basket_total = get_basket_total(session['basket'])
    return render_template_with_basket_quantity('basket.html', items=items, basket_total=basket_total)


@app.route('/checkout/address', methods=['GET', 'POST'])
@initialise_basket
def checkout_address_page():
    form = CheckoutForm()
    if form.validate_on_submit():
        session['address'] = {
            'house': form.house.data,
            'street': form.street.data,
            'city': form.city.data,
            'postcode': form.postcode.data,
        }
        return redirect(url_for('checkout_payment_page'))
    basket_total = get_basket_total(session['basket'])
    house = session['address'].get('house') or '' if 'address' in session else ''
    street = session['address'].get('street') or '' if 'address' in session else ''
    city = session['address'].get('city') or '' if 'address' in session else ''
    postcode = session['address'].get('postcode') or '' if 'address' in session else ''
    return render_template_with_basket_quantity('checkout_address.html', title='Checkout', form=form, basket_total=basket_total,
                                                house=house, street=street, city=city, postcode=postcode)


@app.route('/checkout/address/autofill', methods=['POST'])
def autofill_address():
    form = CheckoutForm()
    if form.is_submitted():
        postcode = form.postcode.data
        street, city = postcode_manager.get_street_and_city_from_postcode(postcode)
        session['address'] = {
            'house': form.house.data,
            'street': street or form.street.data,
            'city': city or form.city.data,
            'postcode': postcode,
        }
    return redirect(url_for('checkout_address_page'))


@app.route('/checkout/payment')
@initialise_basket
def checkout_payment_page():
    if 'address' not in session:
        return redirect(url_for('checkout_address_page'))
    basket_total = get_basket_total(session['basket'])
    return render_template_with_basket_quantity('checkout_payment.html', key=STRIPE_PUBLISHABLE_KEY, basket_total=basket_total)


@app.route('/checkout/complete', methods=['GET', 'POST'])
@initialise_basket
def checkout_complete_page():
    if request.method == 'POST':
        items = get_items_from_basket(session['basket'])
        order = Order(user_id=current_user.id if current_user.is_authenticated else None,
                      date=date.today(),
                      house=session['address']['house'],
                      street=session['address']['street'],
                      city=session['address']['city'],
                      postcode=session['address']['postcode'])
        db.session.add(order)
        db.session.commit()
        for item, quantity in items.items():
            order_item_additions = order_items.insert().values(
                order_id=order.id,
                item_id=item.id,
                quantity=quantity,
            )
            db.session.execute(order_item_additions)
        db.session.commit()
        session['previous_basket'] = session['basket']
        session.pop('basket')
        session.pop('address')
        return redirect(url_for('checkout_complete_page'))
    if 'previous_basket' not in session:
        return redirect(url_for('home_page'))
    items = get_items_from_basket(session['previous_basket'])
    basket_total = get_basket_total(session['previous_basket'])
    return render_template_with_basket_quantity('checkout_complete.html', items=items, basket_total=basket_total)


@app.route('/logout', methods=['POST'])
def logout_page():
    logout_user()
    flash('You have logged out successfully', category='success')
    return redirect(url_for('home_page'))


if __name__ == '__main__':
    app.run(port=5006, debug=True)
