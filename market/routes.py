from market import app
from flask import render_template, redirect, url_for, flash, request
from market.models import User, Drink, Ingredient, Map
from market.forms import RegisterForm, LoginForm, MixDrinkForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")


@app.route("/market", methods=["GET", "POST"]) # drinks
@login_required
def market_page(): #drinks_page
    mix_form = MixDrinkForm()
    #selling_form = SellItemForm()
    if request.method == "POST":
        #Purchase Item
        mixed_drink = request.form.get("purchased_drink")
        m_drink = Drink.query.filter_by(name=mixed_drink).first()
        if m_drink:
            if current_user.can_purchase(m_drink):
                #p_item_object.buy(current_user)
                #try:

                flash(f"Congratulations! Your drink {m_drink.name} will be mixed!", category="success")

                m_drink.mix_drink():

            else: 
                flash(f"Unfortunately, the bartender can't proceed mixin' the {m_drink.name}!", category="danger")
        #Sell Item
        # sold_item = request.form.get('sold_item')
        # s_item_object = Item.query.filter_by(name=sold_item).first()
        # if s_item_object:
        #     if current_user.can_sell(s_item_object):
        #         s_item_object.sell(current_user)
        #         flash(f"Congratulations! Your sold {s_item_object.name} for {s_item_object.price} $ back to market!", category="success")
        #     else: 
        #         flash(f"Unfortunately, something went wrong with selling {s_item_object.name}!", category="danger")

        # return redirect(url_for('market_page'))
    
    if request.method == "GET":
        drinks = Drink.query.order_by(Drink.id.asc()).all()
        list = db.session.query(Drink, Ingredient, Map).filter(Drink.id == Map.drinkID).filter(Map.ingredientID == Ingredient.id).order_by(Drink.id.asc()).all()  

        #items = Item.query.filter_by(owner=None)
        #owned_items= Item.query.filter_by(owner=current_user.id)
        return render_template("market.html", list=list, drinks=drinks, mix_form=mix_form) # drinks.html | owned_items=owned_items, items=items, selling_Form=selling_Form

@app.route("/register", methods=["GET", "POST"])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data, email_address=form.email_address.data, password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logeed in as: {user_to_create.username}", category="success")
        return redirect(url_for("market_page"))
    if form.errors != {}: #wenn keine fehler drin sind von der validation
        for err_msg in form.errors.values():
            flash(f"There was an error with creating a user: {err_msg}", category="danger")

    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f"Success! You are logged in as: {attempted_user.username}", category="success")
            return redirect(url_for("market_page"))
        else:
            flash("Username and Password are not match! Please try again!", category="danger")


    return render_template("login.html", form=form)

@app.route("/logout")
def logout_page():
    logout_user()
    flash("You have been logged out!", category="info")

    return redirect(url_for("home_page"))