from flask import Flask, render_template, session, request, redirect, url_for

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Sample product data (add more as needed)
products = [
    {"id": 1, "name": "Red T-Shirt", "category": "women", "price": 29.99, "image": "red_tshirt.jpg"},
    {"id": 2, "name": "Blue Jeans", "category": "men", "price": 59.99, "image": "blue_jeans.jpg"},
    {"id": 3, "name": "Kids Hoodie", "category": "kids", "price": 39.99, "image": "kids_hoodie.jpg"},
    {"id": 4, "name": "Baby Onesie", "category": "baby", "price": 19.99, "image": "baby_onesie.jpg"},
]

topics = [
    {'id': 1, 'title': 'html', 'body' : 'html is'},
    {'id': 2, 'title': 'css', 'body' : 'css is'},
    {'id': 3, 'title': 'javascript', 'body' : 'javascript is'},

]

@app.route("/")
def home():
    toppings = ['Cheeze', 'Peperoni', 'Mushroom', 14]
    return render_template("index.html", toppings=toppings)

@app.route("/user/<name>/")
def user(name):
    return render_template("user.html", user_name=name)


def home2():
    liTags = ''
    for topic in topics:
        liTags = liTags + f'<li><a href="/read/{topic["id"]}"/>{topic["title"]}</a></li>'
    return f'''
<!doctype html>
<html>
    <body>
        <h1><a href="/">WEB!!</a></h1>
        <ol>
            {liTags}

            <li><a href="/read/1/">html</a></li>
            <li><a href="/read/2/">css</a></li>
            <li><a href="/read/3/">javascript</a></li>
        </ol>
        <h2>Welcome</h2>
        Hello, Web!
    </body>
</html>
    '''


@app.route("/create/")
def create():
    return 'Create'

@app.route("/read/<int:id>/")
def read(id):
    return 'Read' + id


#app.run(port=5001, debug=True)

# @app.route("/products")
# def product_list():
#     category = request.args.get("category")
#     filtered = [p for p in products if p["category"] == category] if category else products
#     utm_query = build_utm_query()
#     return render_template("product_list.html", products=filtered, category=category, utm_query=utm_query)

# @app.route("/product/<int:product_id>")
# def product_detail(product_id):
#     product = next((p for p in products if p["id"] == product_id), None)
#     if not product:
#         return "Product Not Found", 404
#     utm_query = build_utm_query()
#     return render_template("product_detail.html", product=product, utm_query=utm_query)

# @app.route("/add_to_cart/<int:product_id>")
# def add_to_cart(product_id):
#     cart = session.get("cart", {})
#     cart[product_id] = cart.get(product_id, 0) + 1
#     session["cart"] = cart
#     return redirect(request.referrer or url_for("product_list"))

# @app.route("/cart")
# def view_cart():
#     cart = session.get("cart", {})
#     cart_items = []
#     total_price = 0
#     for pid, qty in cart.items():
#         product = next((p for p in products if p["id"] == pid), None)
#         if product:
#             subtotal = product["price"] * qty
#             total_price += subtotal
#             cart_items.append({"product": product, "quantity": qty, "subtotal": subtotal})
#     return render_template("cart.html", cart_items=cart_items, total=total_price)

# @app.route("/update_cart", methods=["POST"])
# def update_cart():
#     cart = session.get("cart", {})
#     for key, val in request.form.items():
#         if key.startswith("quantity_"):
#             pid = int(key.replace("quantity_", ""))
#             qty = max(int(val), 1)
#             cart[pid] = qty
#         elif key.startswith("remove_") and val == "on":
#             pid = int(key.replace("remove_", ""))
#             cart.pop(pid, None)
#     session["cart"] = cart
#     return redirect(url_for("view_cart"))

# @app.route("/checkout")
# def checkout():
#     cart = session.get("cart", {})
#     if not cart:
#         return redirect(url_for("view_cart"))
#     # Normally save order here
#     session["cart"] = {}
#     return render_template("checkout.html")
