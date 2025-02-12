from fastapi import FastAPI

# Import ROuters
from services import (customer, payment_method, product, category, coupons, seller, 
                      offer, orders, product_recommendations, returns, review, search_history,
                       shipping, shopping_cart, shopping_cart_product, order_items)  # Ajusta las rutas si es necesario

app = FastAPI(title="My Amazon API")

# Routers
app.include_router(customer.router)
app.include_router(product.router)
app.include_router(category.router)
app.include_router(coupons.router)
app.include_router(seller.router)
app.include_router(offer.router)
app.include_router(orders.router)
app.include_router(payment_method.router)
app.include_router(product_recommendations.router)
app.include_router(returns.router)
app.include_router(review.router)
app.include_router(search_history.router)
app.include_router(shipping.router)
app.include_router(shopping_cart.router)
app.include_router(shopping_cart_product.router)
app.include_router(order_items.router)

# Puedes agregar más configuración aquí, como middleware, etc.

@app.get("/")  # Ruta raíz
async def root():
    return {"message": "¡Welcome!"}