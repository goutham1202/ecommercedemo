import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:5000"

st.title("Simple E-commerce App")

# Display products
response = requests.get(f"{BASE_URL}/products")
products = response.json()

st.subheader("Products")
for p in products:
    if st.button(f"Add {p['name']} to cart"):
        requests.post(f"{BASE_URL}/cart", json=p)
        st.success(f"{p['name']} added to cart!")

# View cart
if st.button("View Cart"):
    cart = requests.get(f"{BASE_URL}/cart").json()
    st.write(cart)

# Checkout
if st.button("Checkout"):
    res = requests.post(f"{BASE_URL}/checkout").json()
    st.success(f"Order placed! Total: ${res['total']}")
