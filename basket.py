from flask import session, render_template
from models import Item


def initialise_basket(function):
    def function_with_basket(*args, **kwargs):
        if 'basket' not in session or not isinstance(session['basket'], dict):
            session['basket'] = {}
        return function(*args, *kwargs)
    function_with_basket.__name__ = function.__name__
    return function_with_basket


def render_template_with_basket_quantity(*args, **kwargs):
    basket_quantity = sum(session['basket'].values())
    return render_template(*args, **kwargs, basket_quantity=basket_quantity)


def get_items_from_basket():
    basket = session['basket']
    return {Item.query.filter_by(id=item_id).first(): quantity for item_id, quantity in basket.items()}


def increase_item_quantity_in_basket(item_id):
    basket = session['basket']
    corresponding_item = Item.query.filter_by(id=item_id).first()
    if corresponding_item is None:
        print('Not found')
        return
    elif item_id not in basket:
        basket[item_id] = 1
    else:
        basket[item_id] += 1
    session['basket'] = basket


def decrease_item_quantity_in_basket(item_id):
    basket = session['basket']
    if item_id not in basket:
        pass
    elif basket[item_id] == 1:
        basket.pop(item_id)
    else:
        basket[item_id] -= 1
    session['basket'] = basket


def get_basket_total():
    items = get_items_from_basket()
    return sum((item.price * quantity for item, quantity in items.items()))
