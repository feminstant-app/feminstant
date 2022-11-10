from base import stripe


def add_stripe_charge(email, amount, token):
    customer = stripe.Customer.create(
        email=email,
        source=token,
    )
    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount * 100,
        currency='gbp',
        description='FemInstant Purchase'
    )
