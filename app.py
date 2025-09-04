from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample in-memory product list
products = [
    {"id": 1, "name": "Laptop", "price": 1200},
    {"id": 2, "name": "Phone", "price": 700},
    {"id": 3, "name": "Headphones", "price": 150}
]

cart = []

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)

@app.route('/cart', methods=['GET', 'POST'])
def manage_cart():
    global cart
    if request.method == 'POST':
        item = request.json
        cart.append(item)
        return jsonify({"message": "Added to cart", "cart": cart})
    else:
        return jsonify(cart)

@app.route('/checkout', methods=['POST'])
def checkout():
    global cart
    total = sum(item['price'] for item in cart)
    cart = []
    return jsonify({"message": "Order placed", "total": total})

if __name__ == "__main__":
    app.run(debug=True)
