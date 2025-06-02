from flask import Flask, render_template, session, request, redirect, url_for, flash

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config['SECRET_KEY'] = "my_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db"

db = SQLAlchemy(app)

class NamerForm(FlaskForm):
    name = StringField("What's your name", validators=[DataRequired()])
    submit = SubmitField("Submit")

class UserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")

class UserLoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), nullable=False, unique=True)
    name = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(256), nullable=False, unique=True)
    data_added = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return '<Name %% >' % self.name

    
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user_login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


# Sample product data (add more as needed)
products = [
    {"id": 1,  "sku": "SKU-001", "name": "Black Dress", "category": "women", "price": 29.99, "image": "women_black.png", "description": "Fancy black dress for women."},
    {"id": 2,  "sku": "SKU-002", "name": "Blue Dress", "category": "women", "price": 59.99, "image": "women_blue.png", "description": "Fancy blue dress for women."},
    {"id": 3,  "sku": "SKU-003", "name": "Pink Dress", "category": "women", "price": 39.99, "image": "women_pink.png", "description": "Fancy pink dress for women."},
    {"id": 4,  "sku": "SKU-004", "name": "White Dress", "category": "women", "price": 19.99, "image": "women_white.png", "description": "Fancy white dress for women."},

    {"id": 5,  "sku": "SKU-005", "name": "Blue T-shirt", "category": "men", "price": 59.99, "image": "men_blue.png", "description": "Cool blue T-shirt for men."},
    {"id": 6,  "sku": "SKU-006", "name": "Gray T-shirt", "category": "men", "price": 39.99, "image": "men_gray.png", "description": "Cool gray T-shirt for men."},
    {"id": 7,  "sku": "SKU-007", "name": "Green T-shirt", "category": "men", "price": 19.99, "image": "men_green.png", "description": "Cool green T-shirt for men."},
    {"id": 8,  "sku": "SKU-008", "name": "White T-shirt", "category": "men", "price": 29.99, "image": "men_white.png", "description": "Cool white T-shirt for men."},

    {"id": 9,  "sku": "SKU-009", "name": "Black T-shirt for Kids", "category": "kids", "price": 29.99, "image": "kids_black.png", "description": "Cute black T-shirt for kids."},
    {"id": 10, "sku": "SKU-010", "name": "Blue T-shirt for Kids", "category": "kids", "price": 59.99, "image": "kids_blue.png", "description": "Cute blue T-shirt for kids."},
    {"id": 11, "sku": "SKU-011", "name": "Green T-shirt for Kids", "category": "kids", "price": 39.99, "image": "kids_green.png", "description": "Cute green T-shirt for kids."},
    {"id": 12, "sku": "SKU-012", "name": "Red T-shirt for Kids", "category": "kids", "price": 19.99, "image": "kids_red.png", "description": "Cute red T-shirt for kids."},

    {"id": 13, "sku": "SKU-012", "name": "Green T-shirt for Baby", "category": "kids", "price": 29.99, "image": "baby_green.png", "description": "Cute green T-shirt for baby."},
    {"id": 14, "sku": "SKU-014", "name": "Pink T-shirt for Baby", "category": "kids", "price": 59.99, "image": "baby_pink.png", "description": "Cute pink T-shirt for baby."},
    {"id": 15, "sku": "SKU-015", "name": "Red T-shirt for Baby", "category": "kids", "price": 39.99, "image": "baby_red.png", "description": "Cute red T-shirt for baby."},
    {"id": 16, "sku": "SKU-016", "name": "Yellow T-shirt for Baby", "category": "kids", "price": 19.99, "image": "baby_yellow.png", "description": "Cute yellow T-shirt for baby."},

]

@app.template_filter('format_currency')
def format_currency_filter(value):
    """
    """
    if isinstance(value, (int, float)):
        return f"{value:,.0f}" 
    return str(value) 

topics = [
    {'id': 1, 'title': 'html', 'body' : 'html is'},
    {'id': 2, 'title': 'css', 'body' : 'css is'},
    {'id': 3, 'title': 'javascript', 'body' : 'javascript is'},

]

@app.route("/")
def home():
    #toppings = ['Cheeze', 'Peperoni', 'Mushroom', 14]
    current_query_params = request.args.to_dict()

    current_user.is_authenticated
    print("current_user.is_authenticated: ", current_user.is_authenticated)
    # if current_user.is_authenticated:
    #     print("current_user.username: ", current_user.username)
    #     print("current_user.name: ", current_user.name)


    return render_template("index.html", products=products, current_user=current_user, query_params=current_query_params)


@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """
    Product Details
    """
    current_query_params = request.args.to_dict()

    product = next((item for item in products if item["id"] == product_id), None)
    if product:
        current_query_params = request.args.to_dict()
        return render_template('product_detail.html', product=product, query_params=current_query_params)
    else:
        return "Cannot find the product.", 404


@app.route('/purchase/<int:product_id>')
def purchase_detail(product_id):
    current_query_params = request.args.to_dict()
    product = next((item for item in products if item["id"] == product_id), None)
    if product:
        current_query_params = request.args.to_dict()
        return render_template('purchase_detail.html', product=product, query_params=current_query_params)
    else:
        return "Cannot find the product.", 404

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart_detail(product_id):
    current_query_params = request.args.to_dict()
    product = next((item for item in products if item["id"] == product_id), None)
    if product:
        current_query_params = request.args.to_dict()
        return render_template('add_to_cart_detail.html', product=product, query_params=current_query_params)
    else:
        return "Cannot find the product.", 404

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

@app.route("/name/", methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('name.html', name=name, form=form)

@app.route("/user_signup/", methods=['GET', 'POST'])
def user_signup():
    current_query_params = request.args.to_dict()
    username = None
    name = None
    email = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(username=form.username.data, name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        username = form.username.data
        name = form.name.data
        form.username.data = ''
        form.name.data = ''
        form.email.data = ''
        flash("User Signed Up Successfully.")
    
    our_users = Users.query.order_by(Users.data_added)
    #print(our_users)
    return render_template('user_signup.html', form=form, username=username, name=name, email=email, our_users=our_users, current_user=current_user, query_params=current_query_params)


@app.route("/user_update/<int:id>", methods=['GET', 'POST'])
def user_update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        try:
            db.session.commit()
            #flash("User updated successfully.")
            return render_template('user_update.html', form=form, name_to_update=name_to_update)
        except:
            #flash("Error.")
            return render_template('user_update.html', form=form, name_to_update=name_to_update)
    else:
        return render_template('user_update.html', form=form, name_to_update=name_to_update)


@app.route("/user_login/", methods=['GET', 'POST'])
def user_login():
    current_query_params = request.args.to_dict()
    username = None
    name = None
    email = None
    form = UserLoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            if form.username.data == form.password.data:
                login_user(user)
                #return redirect(url_for('user_dashboard', username=user.username))
                return render_template('user_dashboard.html', username=user.username, name=user.name, email=user.email, current_user=current_user, query_params=current_query_params)
            else:
                flash('Error')

        # username = form.username.data
        # password = form.password.data
        form.username.data = ''
        form.password.data = ''
        flash("User Login Successfully.")

    our_users = Users.query.order_by(Users.data_added)
    #print(our_users)
    return render_template('user_login.html', form=form, username=username, name=name, our_users=our_users, current_user=current_user, query_params=current_query_params)

@app.route("/user_logout/", methods=['GET', 'POST'])
@login_required    
def user_logout():
    current_query_params = request.args.to_dict()
    logout_user()
    flash('User are logged out.')

    #return redirect(url_for('user_login', **current_query_params))
    return render_template('user_logout.html', current_user=current_user, query_params=current_query_params)



@app.route("/user_dashboard/", methods=['GET', 'POST'])
@login_required
def user_dashboard():
    print('current_user.username')
    print(current_user.username)

    return render_template('user_dashboard.html')

#app.run(port=5001, debug=True)

