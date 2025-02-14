import mysql.connector
import random
from faker import Faker

"""Database connection"""
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin123",
    database="amazon-db",
    port="3306"
)
cur = conn.cursor()

"""Faker instance"""
fake = Faker()

"""Data generation"""

"""1. Tables without foreign keys"""

"""Table customer"""
for _ in range(50):
    full_name = fake.name()
    email = fake.email()
    shipping_address = fake.address()
    phone = fake.phone_number()
    if len(phone) > 15:
        phone = phone[:15]  # Truncate to 15 characters
    registration_date = fake.date_between(start_date='-1y', end_date='today')
    cur.execute("INSERT INTO Customer (full_name, email, shipping_address, phone, registration_date) VALUES (%s, %s, %s, %s, %s)", (full_name, email, shipping_address, phone, registration_date))

"""Table category"""
for _ in range(10):
    category_name = fake.word().capitalize()
    description = fake.text()
    cur.execute("INSERT INTO Category (categoryName, description) VALUES (%s, %s)", (category_name, description))

"""Table seller"""
for _ in range(20):
    seller_name = fake.company()
    seller_type = random.choice(["Mayorista", "Minorista", "Online"])
    seller_rating = round(random.uniform(1, 5), 2)
    cur.execute("INSERT INTO Seller (seller_name, seller_type, seller_rating) VALUES (%s, %s, %s)", (seller_name, seller_type, seller_rating))

"""Table payment_method"""
for _ in range(20):
    payment_type = random.choice(["Tarjeta de crédito", "PayPal", "Transferencia bancaria"])
    cur.execute("INSERT INTO Payment_Method (payment_type) VALUES (%s)", (payment_type,))

"""Table shipping"""
for _ in range(40):
    shipping_company = fake.company()
    shipping_cost = round(random.uniform(5, 50), 2)
    cur.execute("INSERT INTO Shipping (shipping_company, shipping_cost) VALUES (%s, %s)", (shipping_company, shipping_cost))

"""Table offer"""
for _ in range(10):
    discount = round(random.uniform(5, 50), 2)
    start_date = fake.date_between(start_date='-1y', end_date='today')
    end_date = fake.date_between(start_date=start_date, end_date='+1y')
    cur.execute("INSERT INTO Offer (discount, start_date, end_date) VALUES (%s, %s, %s)", (discount, start_date, end_date))

"""2. Get IDs from related tables"""

cur.execute("SELECT customer_id FROM Customer")
customer_ids = [row[0] for row in cur.fetchall()]
cur.execute("SELECT category_id FROM Category")
category_ids = [row[0] for row in cur.fetchall()]
cur.execute("SELECT seller_id FROM Seller")
seller_ids = [row[0] for row in cur.fetchall()]
cur.execute("SELECT payment_method_id FROM Payment_Method")
payment_method_ids = [row[0] for row in cur.fetchall()]
cur.execute("SELECT shipping_id FROM Shipping")
shipping_ids = [row[0] for row in cur.fetchall()]
cur.execute("SELECT coupons_id FROM Coupons")
coupon_ids = [row[0] for row in cur.fetchall()]
cur.execute("SELECT offer_id FROM Offer")
offer_ids = [row[0] for row in cur.fetchall()]

"""3. Tables with foreign keys"""

"""Table product"""
for _ in range(80):
    product_name = fake.catch_phrase()
    description = fake.text()
    price = round(random.uniform(10, 1000), 2)
    quantity_available = random.randint(0, 100)
    category_id = random.choice(category_ids)
    seller_id = random.choice(seller_ids)
    cur.execute("INSERT INTO Product (product_name, description, price, quantity_available, category_id, seller_id) VALUES (%s, %s, %s, %s, %s, %s)", (product_name, description, price, quantity_available, category_id, seller_id))

"""Table coupons"""
for _ in range(50):
    discount_code = fake.ean(length=13)  # Random coupon code (adjust as needed)
    discount_value = random.randint(5, 50)  # Discount between 5% and 50%
    expiration_date = fake.date_between(start_date='+1w', end_date='+1y')  # Expires between 1 week and 1 year
    cur.execute("INSERT INTO Coupons (discount_code, discount_value, expiration_date) VALUES (%s, %s, %s)", (discount_code, discount_value, expiration_date))

"""Get IDs from coupons"""
cur.execute("SELECT coupons_id FROM Coupons")
coupon_ids = [row[0] for row in cur.fetchall()]

"""Table orders"""
for _ in range(40):
    total_amount = round(random.uniform(50, 5000), 2)
    order_status = random.choice(["Pendiente", "En proceso", "Enviado", "Entregado"])
    customer_id = random.choice(customer_ids)
    payment_method_id = random.choice(payment_method_ids)
    shipping_id = random.choice(shipping_ids)
    order_date = fake.date_between(start_date='-1y', end_date='today')
    cur.execute("INSERT INTO Orders (total_amount, order_status, customer_id, payment_method_id, shipping_id) VALUES (%s, %s, %s, %s, %s)", (total_amount, order_status, customer_id, payment_method_id, shipping_id))

"""Get IDs from orders and products for order_items"""
cur.execute("SELECT orders_id FROM Orders")
order_ids = [row[0] for row in cur.fetchall()]
cur.execute("SELECT product_id FROM Product")
product_ids = [row[0] for row in cur.fetchall()]

"""Table order_items"""
for _ in range(100):
    orders_id = random.choice(order_ids)
    product_id = random.choice(product_ids)
    quantity = random.randint(1, 10)
    price_at_purchase = round(random.uniform(10, 1000), 2)
    coupon_id = random.choice([None] + coupon_ids)  # Ensure coupon_id is either None or a valid ID
    offer_id = random.choice([None] + offer_ids)  # Ensure offer_id is either None or a valid ID
    cur.execute("INSERT INTO Order_Items (orders_id, product_id, quantity, price_at_purchase, coupon_id, offer_id) VALUES (%s, %s, %s, %s, %s, %s)", (orders_id, product_id, quantity, price_at_purchase, coupon_id, offer_id))

"""Table review"""
for _ in range(30):
    rating = random.randint(1, 5)
    comment = fake.text()
    review_date = fake.date_between(start_date='-1y', end_date='today')
    customer_id = random.choice(customer_ids)
    cur.execute("INSERT INTO Review (rating, comment, review_date, customer_id) VALUES (%s, %s, %s, %s)", (rating, comment, review_date, customer_id))

"""Table product_recommendations"""
for _ in range(40):
    customer_id = random.choice(customer_ids)
    cur.execute("INSERT INTO Product_Recommendations (customer_id) VALUES (%s)", (customer_id,))

"""Table returns"""
for _ in range(10):
    return_date = fake.date_between(start_date='-1y', end_date='today')
    return_reason = fake.text()
    return_status = random.choice(["Pendiente", "Aprobado", "Rechazado"])
    cur.execute("INSERT INTO Returns (return_date, return_reason, return_status) VALUES (%s, %s, %s)", (return_date, return_reason, return_status))

"""Table search_history"""
for _ in range(50):
    search_term = fake.word()
    search_date = fake.date_between(start_date='-1y', end_date='today')
    customer_id = random.choice(customer_ids)
    cur.execute("INSERT INTO Search_History (search_term, search_date, customer_id) VALUES (%s, %s, %s)", (search_term, search_date, customer_id))

"""Table shopping_cart"""
for _ in range(30):
    customer_id = random.choice(customer_ids)
    cur.execute("INSERT INTO Shopping_Cart (customer_id) VALUES (%s)", (customer_id,))

"""Table shopping_cart_product"""
cur.execute("SELECT shopping_cart_id FROM Shopping_Cart")
shopping_cart_ids = [row[0] for row in cur.fetchall()]
cur.execute("SELECT product_id FROM Product")
product_ids = [row[0] for row in cur.fetchall()]

cart_product_combinations = set()

for _ in range(80):
    while True:
        cart_id = random.choice(shopping_cart_ids)
        product_id = random.choice(product_ids)
        if (cart_id, product_id) not in cart_product_combinations:
            cart_product_combinations.add((cart_id, product_id))
            break

    quantity = random.randint(1, 10)
    cur.execute("INSERT INTO Shopping_Cart_Product (cart_id, product_id, quantity) VALUES (%s, %s, %s)", (cart_id, product_id, quantity))

"""4. Update tables with pending foreign keys"""

"""Table payment_method (now with customer_id)"""
for payment_method_id in payment_method_ids:
    customer_id = random.choice(customer_ids)
    cur.execute("UPDATE Payment_Method SET customer_id = %s WHERE payment_method_id = %s", (customer_id, payment_method_id))

"""Table shipping (now with shipping_date and estimated_delivery)"""
for shipping_id in shipping_ids:
    shipping_date = fake.date_between(start_date='-1w', end_date='today')
    estimated_delivery = fake.date_between(start_date=shipping_date, end_date='+2w')
    cur.execute("UPDATE Shipping SET shipping_date = %s, estimated_delivery = %s WHERE shipping_id = %s", (shipping_date, estimated_delivery, shipping_id))

"""Table review (now with product_id)"""
cur.execute("SELECT review_id FROM Review")
review_ids = [row[0] for row in cur.fetchall()]

for review_id in review_ids:
    product_id = random.choice(product_ids)
    cur.execute("UPDATE Review SET product_id = %s WHERE review_id = %s", (product_id, review_id))

"""Table product_recommendations (now with recommended_product_id)"""
cur.execute("SELECT product_recommendation_id FROM Product_Recommendations")
product_recommendation_ids = [row[0] for row in cur.fetchall()]

for product_recommendation_id in product_recommendation_ids:
    recommended_product_id = random.choice(product_ids)
    cur.execute("UPDATE Product_Recommendations SET recommended_product_id = %s WHERE product_recommendation_id = %s", (recommended_product_id, product_recommendation_id))

"""Table returns (now with order_item_id)"""
cur.execute("SELECT returns_id FROM Returns")
return_ids = [row[0] for row in cur.fetchall()]
cur.execute("SELECT order_item_id FROM Order_Items")
order_item_ids = [row[0] for row in cur.fetchall()]

for return_id in return_ids:
    order_item_id = random.choice(order_item_ids)
    cur.execute("UPDATE Returns SET order_item_id = %s WHERE returns_id = %s", (order_item_id, return_id))

"""Save changes and close connection"""
conn.commit()
cur.close()
conn.close()

print("Data generated and inserted successfully.")