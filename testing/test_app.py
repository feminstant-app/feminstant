from unittest import TestCase, main
from app import app


class TestApp(TestCase):

    def test_home_page(self):
        with app.test_client() as client:
            response = client.get('/')
            self.assertIn("Feminine products in an Instant", response.text)

    def test_about_page(self):
        with app.test_client() as client:
            response = client.get('/about')
            self.assertIn("Happy Shopping FemInstant Fam", response.text)

    def test_products_page(self):
        with app.test_client() as client:
            response = client.get('/products')
            self.assertIn("Add to basket", response.text)

    def test_basket_page(self):
        with app.test_client() as client:
            response = client.get('/basket')
            self.assertIn("Your Basket", response.text)

    def test_checkout_address_page(self):
        with app.test_client() as client:
            response = client.get('/checkout/address')
            self.assertIn("You are about to purchase", response.text)

    def test_checkout_payment_page(self):
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['address'] = {'house': '1', 'street': 'Brian Close', 'city': 'Chelmsford', 'postcode': 'CM2 9ES'}
            response = client.get('/checkout/payment')
            self.assertIn("Thanks, please pay", response.text)

    def test_checkout_complete_page(self):
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['previous_basket'] = {}
            response = client.get('/checkout/complete')
            self.assertIn("Thanks for your order!", response.text)


if __name__ == '__main__':
    main()
