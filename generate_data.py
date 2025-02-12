import psycopg2
import random
from faker import Faker

# --- Conexión a la base de datos ---
conn = psycopg2.connect("dbname=amazon user=postgres password=admin123")  # Reemplaza con tus credenciales
cur = conn.cursor()

# --- Instancia de Faker ---
fake = Faker()

# --- Generación de datos ---

# 1. Tablas sin claves foráneas

# Tabla customer
for _ in range(50):
    full_name = fake.name()
    email = fake.email()
    shipping_address = fake.address()
    phone = fake.phone_number()
    if len(phone) > 15:
        phone = phone[:15]  # Truncar a 15 caracteres
        # O podrías simplemente omitir la inserción:
        # continue
    registration_date = fake.date_between(start_date='-1y', end_date='today')
    cur.execute("INSERT INTO customer (full_name, email, shipping_address, phone, registration_date) VALUES (%s, %s, %s, %s, %s)", (full_name, email, shipping_address, phone, registration_date))

# Tabla category
for _ in range(10):
    category_name = fake.word().capitalize()
    description = fake.text()
    cur.execute("INSERT INTO category (categoryName, description) VALUES (%s, %s)", (category_name, description))

# Tabla seller
for _ in range(20):
    seller_name = fake.company()
    seller_type = random.choice(["Mayorista", "Minorista", "Online"])
    seller_rating = round(random.uniform(1, 5), 2)
    cur.execute("INSERT INTO seller (seller_name, seller_type, seller_rating) VALUES (%s, %s, %s)", (seller_name, seller_type, seller_rating))

# Tabla payment_method
for _ in range(20):
    payment_type = random.choice(["Tarjeta de crédito", "PayPal", "Transferencia bancaria"])
    # customer_id (clave foránea) se asignará después
    cur.execute("INSERT INTO payment_method (payment_type) VALUES (%s)", (payment_type,))

# Tabla shipping
for _ in range(40):
    shipping_company = fake.company()
    # shipping_date y estimated_delivery se asignarán después
    shipping_cost = round(random.uniform(5, 50), 2)
    cur.execute("INSERT INTO shipping (shipping_company, shipping_cost) VALUES (%s, %s)", (shipping_company, shipping_cost))

# 2. Obtener IDs de tablas relacionadas

cur.execute("SELECT customer_id FROM customer")
customer_ids = [row[0] for row in cur.fetchall()]
cur.execute("SELECT category_id FROM category")
category_ids = [row[0] for row in cur.fetchall()]
cur.execute("SELECT seller_id FROM seller")
seller_ids = [row[0] for row in cur.fetchall()]
cur.execute("SELECT payment_method_id FROM payment_method")
payment_method_ids = [row[0] for row in cur.fetchall()]
cur.execute("SELECT shipping_id FROM shipping")
shipping_ids = [row[0] for row in cur.fetchall()]

# 3. Tablas con claves foráneas

# Tabla product
for _ in range(80):
    product_name = fake.catch_phrase()
    description = fake.text()
    price = round(random.uniform(10, 1000), 2)
    quantity_available = random.randint(0, 100)
    category_id = random.choice(category_ids)
    seller_id = random.choice(seller_ids)
    cur.execute("INSERT INTO product (product_name, description, price, quantity_available, category_id, seller_id) VALUES (%s, %s, %s, %s, %s, %s)", (product_name, description, price, quantity_available, category_id, seller_id))

# Tabla coupons
for _ in range(50):
    coupon_code = fake.ean(length=13)  # Código de cupón aleatorio (puedes ajustarlo)
    discount_percentage = random.randint(5, 50)  # Descuento entre 5% y 50%
    expiry_date = fake.date_between(start_date='+1w', end_date='+1y')  # Expira en 1 semana y 1 año
    cur.execute("INSERT INTO coupons (coupon_code, discount_percentage, expiry_date) VALUES (%s, %s, %s)", (coupon_code, discount_percentage, expiry_date))

# Tabla orders
for _ in range(40):
    total_amount = round(random.uniform(50, 5000), 2)
    order_status = random.choice(["Pendiente", "En proceso", "Enviado", "Entregado"])
    customer_id = random.choice(customer_ids)
    payment_method_id = random.choice(payment_method_ids)
    shipping_id = random.choice(shipping_ids)
    order_date = fake.date_between(start_date='-1y', end_date='today')
    cur.execute("INSERT INTO orders (total_amount, order_status, customer_id, payment_method_id, shipping_id) VALUES (%s, %s, %s, %s, %s)", (total_amount, order_status, customer_id, payment_method_id, shipping_id))

# Tabla review
for _ in range(30):
    rating = random.randint(1, 5)
    comment = fake.text()
    review_date = fake.date_between(start_date='-1y', end_date='today')
    customer_id = random.choice(customer_ids)
    # product_id (clave foránea) se asignará después
    cur.execute("INSERT INTO review (rating, comment, review_date, customer_id) VALUES (%s, %s, %s, %s)", (rating, comment, review_date, customer_id))

# Tabla product_recommendations
for _ in range(40):
    customer_id = random.choice(customer_ids)
    # recommended_product_id (clave foránea) se asignará después
    cur.execute("INSERT INTO product_recommendations (customer_id) VALUES (%s)", (customer_id,))

# Tabla returns
for _ in range(10):
    return_date = fake.date_between(start_date='-1y', end_date='today')
    return_reason = fake.text()
    return_status = random.choice(["Pendiente", "Aprobado", "Rechazado"])
    # orders_id (clave foránea) se asignará después
    cur.execute("INSERT INTO returns (return_date, return_reason, return_status) VALUES (%s, %s, %s)", (return_date, return_reason, return_status))

# Tabla search_history
for _ in range(50):
    search_term = fake.word()
    search_date = fake.date_between(start_date='-1y', end_date='today')
    customer_id = random.choice(customer_ids)
    cur.execute("INSERT INTO search_history (search_term, search_date, customer_id) VALUES (%s, %s, %s)", (search_term, search_date, customer_id))

# Tabla shopping_cart
for _ in range(30):
    customer_id = random.choice(customer_ids)
    cur.execute("INSERT INTO shopping_cart (customer_id) VALUES (%s)", (customer_id,))

# Tabla shopping_cart_product
# Esta tabla necesita datos en shopping_cart y product
cur.execute("SELECT shoppingCart_id FROM shopping_cart")
shopping_cart_ids = [row[0] for row in cur.fetchall()]
cur.execute("SELECT product_id FROM product")
product_ids = [row[0] for row in cur.fetchall()]

for _ in range(80):
    cart_id = random.choice(shopping_cart_ids)
    product_id = random.choice(product_ids)
    quantity = random.randint(1, 10)

cart_product_combinations = set()  # Conjunto para almacenar combinaciones únicas

for _ in range(80):
    while True: #Bucle hasta encontrar una combinación única.
        cart_id = random.choice(shopping_cart_ids)
        product_id = random.choice(product_ids)
        if (cart_id, product_id) not in cart_product_combinations:
            cart_product_combinations.add((cart_id, product_id))
            break #Sale del bucle while si la combinación es única.

    quantity = random.randint(1, 10)
    cur.execute("INSERT INTO shopping_cart_product (cart_id, product_id, quantity) VALUES (%s, %s, %s)", (cart_id, product_id, quantity))

# 4. Actualizar tablas con claves foráneas pendientes

# Tabla payment_method (ahora con customer_id)
for payment_method_id in payment_method_ids:
    customer_id = random.choice(customer_ids)
    cur.execute("UPDATE payment_method SET customer_id = %s WHERE payment_method_id = %s", (customer_id, payment_method_id))

# Tabla shipping (ahora con shipping_date y estimated_delivery)
for shipping_id in shipping_ids:
    shipping_date = fake.date_between(start_date='-1w', end_date='today')
    estimated_delivery = fake.date_between(start_date=shipping_date, end_date='+2w')
    cur.execute("UPDATE shipping SET shipping_date = %s, estimated_delivery = %s WHERE shipping_id = %s", (shipping_date, estimated_delivery, shipping_id))

# Tabla review (ahora con product_id)
cur.execute("SELECT review_id FROM review")
review_ids = [row[0] for row in cur.fetchall()]

for review_id in review_ids:
    product_id = random.choice(product_ids)  # Elige un product_id aleatorio
    cur.execute("UPDATE review SET product_id = %s WHERE review_id = %s", (product_id, review_id))

# Tabla product_recommendations (ahora con recommended_product_id)
cur.execute("SELECT productRecommendation_id FROM product_recommendations")
product_recommendation_ids = [row[0] for row in cur.fetchall()]

for product_recommendation_id in product_recommendation_ids:
    recommended_product_id = random.choice(product_ids)
    cur.execute("UPDATE product_recommendations SET recommended_product_id = %s WHERE productRecommendation_id = %s", (recommended_product_id, product_recommendation_id))

# Tabla returns (ahora con orders_id)
cur.execute("SELECT returns_id FROM returns")
return_ids = [row[0] for row in cur.fetchall()]
cur.execute("SELECT orders_id FROM orders")
order_ids = [row[0] for row in cur.fetchall()]

for return_id in return_ids:
    order_id = random.choice(order_ids)
    cur.execute("UPDATE returns SET orders_id = %s WHERE returns_id = %s", (order_id, return_id))


# --- Guardar cambios y cerrar conexión ---
conn.commit()
cur.close()
conn.close()

print("Datos generados e insertados correctamente.")