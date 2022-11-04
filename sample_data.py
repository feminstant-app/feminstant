from app import app, db, Item, Employee, Customer

with app.app_context():
    items = [
        Item(name='CeraVe Hydrating Cleanser with Hyaluronic Acid 236ml', quantity=59, price=9.99, department='Skincare', description='hydrating cleanser for normal to dry skin'),
        Item(name='Simple Kind To Skin Cleansing Wipes Biodegradable X50', quantity=110, price=3.00, department='Skincare', description='Gentle cleansing wipes'),
        Item(name='Simple Kind to Skin Refreshing Facial Wash Gel 50ml', quantity=82, price=1.50, department='Skincare', description='Gentle cleansing facial wash'),
        Item(name='CeraVe Moisturising Lotion For Dry to Very Dry Skin 236ml', quantity=110, price=9.99, department='Skincare', description='Moisturising lotion for dry skin'),
        Item(name='Burts Bees Beeswax Lip Balm 4.25g', quantity=80, price=3.99, department='Skincare', description='Hydrating lip balm'),
        Item(name='NYX Professional Makeup Setting Spray Matte', quantity=92, price=8.00, department='Makeup', description='Setting spray'),
        Item(name='Maybelline Instant Conceal Eraser Concealer Nude', quantity=52, price=8.99, department='Makeup', description='perfect the under eye area, covering flawlessly'),
        Item(name='NYX Professional Makeup Micro Brow Pencil', quantity=97, price=8.00, department='Makeup', description='Brow pencil'),
        Item(name='NYX Professional Makeup Butter Gloss - Praline', quantity=50, price=6.50, department='Makeup', description='soft and silky smooth lip gloss.'),
        Item(name='Maybelline Lash Sensational Sky High Mascara 01 Black', quantity=57, price=11.99, department='Makeup', description='Lengthens and volumises the lashes'),
        Item(name='Always Maxi Long Plus Sanitary Towels x12', quantity=125, price=1.99, department='Feminine Hygiene', description='Maximum protection for heavier flow'),
        Item(name='Always Ultra Secure Night Duo Sanitary Towels Multipack 18', quantity=105, price=2.85, department='Feminine Hygiene', description='Up to 10 hours of protection'),
        Item(name='Always Sensitive Normal Ultra (Size 1) Sanitary Towels x16', quantity=105, price=1.55, department='Feminine Hygiene', description='Ideal for delicate skin'),
        Item(name='Tampax Compak Regular Tampons 18', quantity=85, price=6.50, department='Feminine Hygiene', description='Regular sized tampons'),
        Item(name='OrganiCup, Size A, Menstrual Cup, 1 uni', quantity=57, price=20.00, department='Feminine Hygiene', description='Can be worn for up to 12 hours')
    ]

    for item in items:
        db.session.add(item)
    db.session.commit()

    employees = [
        Employee(name='Sam Jones'),
        Employee(name='John Smith'),
        Employee(name='Tom Morgan'),
        Employee(name='James Harding'),
    ]

    for employee in employees:
        db.session.add(employee)
    db.session.commit()

    customers = [
        Customer(user_name='ASmith', password='password', customer_name='Alana Smith', customer_email='alanas@gmail.com',
        location='North London'),
        Customer(user_name='WEdwards', password='password', customer_name='Winta Edwards', customer_email='wintae@gmail.com',
        location='West London')
    ]
    for customer in customers:
        db.session.add(customer)
    db.session.commit()
