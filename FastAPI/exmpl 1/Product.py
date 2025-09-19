from fastapi import FastAPI,HTTPException
from schema import ProductBase


app=FastAPI()


@app.post('/Product')
def Create_Product(product:ProductBase):
    return product
