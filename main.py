from fastapi import FastAPI

# Import ROuters
from services import customer, product, category  # Ajusta las rutas si es necesario

app = FastAPI(title="My Amazon API")

# Routers
app.include_router(customer.router)
app.include_router(product.router)
app.include_router(category.router)

# Puedes agregar más configuración aquí, como middleware, etc.

@app.get("/")  # Ruta raíz
async def root():
    return {"message": "¡Welcome!"}