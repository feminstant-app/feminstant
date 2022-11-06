import stripe

from config import STRIPE_SECRET_KEY, STRIPE_PUBLISHABLE_KEY

stripe_keys = {
  'secret_key': [STRIPE_SECRET_KEY],
  'publishable_key': [STRIPE_PUBLISHABLE_KEY]
}

stripe.api_key = stripe_keys['secret_key']
