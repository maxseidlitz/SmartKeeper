from drinks import app
from flask import render_template, redirect, url_for, flash, request
from drinks.models import User, Drink, Ingredient, Map
from drinks.forms import RegisterForm, LoginForm, MixDrinkForm, AddDrinkForm, AddIngredientForm
from drinks import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")


@app.route("/drinks", methods=["GET", "POST"])
@login_required
def drinks_page():
    mix_form = MixDrinkForm()
    addIngredient_form = AddIngredientForm()

    _list = db.session.query(Ingredient.name).all()
    list = [value for value, in _list]

    addDrink_form = AddDrinkForm()
    addDrink_form.ingredientChoice_1.choices = list

    if request.method == "POST":

        if addDrink_form.submit_AddDrink.data: # notice the submit button of specific form |  and addDrink_form.validate()
            drink_to_create = Drink(name=addDrink_form.name.data, description=addDrink_form.description.data)
            db.session.add(drink_to_create)
            db.session.commit()
            
            r1 = addDrink_form.ratio_1.data
            r2 = addDrink_form.ratio_2.data
            r3 = addDrink_form.ratio_3.data

            i1 = addDrink_form.ingredientChoice_1.data
            i2 = addDrink_form.ingredientChoice_2.data
            i3 = addDrink_form.ingredientChoice_3.data

            i_1 = db.session.query(Ingredient).filter_by(name=i1).first()
            i_2 = db.session.query(Ingredient).filter_by(name=i2).first()
            i_3 = db.session.query(Ingredient).filter_by(name=i3).first()

            map_ratio_1 = Map(ratio=r1,drinkID=drink_to_create.id, ingredientID=i_1.id)
            map_ratio_2 = Map(ratio=r2,drinkID=drink_to_create.id, ingredientID=i_2.id)
            map_ratio_3 = Map(ratio=r3,drinkID=drink_to_create.id, ingredientID=i_3.id)
            
            db.session.add(map_ratio_1)
            db.session.add(map_ratio_2)
            db.session.add(map_ratio_3)
            db.session.commit()
            
            return redirect(url_for("drinks_page"))
        
        if addIngredient_form.submit_AddIngredient.data: # notice the submit button of specific form |  and addIngredient_form.validate()
            ingredient_to_create = Ingredient(name=addIngredient_form.name.data,percentage=addIngredient_form.percentage.data,pump=addIngredient_form.pump.data)
            db.session.add(ingredient_to_create)
            db.session.commit()

            return redirect(url_for("drinks_page"))

        if mix_form.submit_MixDrink.data: # and mix_form.validate()
            # Mix Drink
            mixed_drink = request.form.get("purchased_drink")
            m_drink = Drink.query.filter_by(name=mixed_drink).first()
            if m_drink:
                # if drink AND ingredients are available

                    flash(f"Congratulations! Your drink {m_drink.name} will be mixed!", category="success")

                    m_drink.mix_drink()

                    return redirect(url_for('drinks_page'))
        if addIngredient_form.errors or addDrink_form or mix_form != {}: #wenn keine fehler drin sind von der validation
            for err_msg in addIngredient_form.errors.values():
                flash(f"There was an error with creating an ingredient: {err_msg}", category="danger")

            for err_msg in addDrink_form.errors.values():
                flash(f"There was an error with creating an drink: {err_msg}", category="danger")

            for err_msg in mix_form.errors.values():
                flash(f"There was an error with mixing the drink: {err_msg}", category="danger")

    if request.method == "GET":
        drinks = Drink.query.order_by(Drink.id.asc()).all()
        list = db.session.query(Drink, Ingredient, Map).filter(Drink.id == Map.drinkID).filter(Map.ingredientID == Ingredient.id).order_by(Drink.id.asc()).all()
        return render_template("drinks.html", list=list, drinks=drinks, mix_form=mix_form, addDrink_form=addDrink_form, addIngredient_form=addIngredient_form)

@app.route("/register", methods=["GET", "POST"])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data, email_address=form.email_address.data, password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logeed in as: {user_to_create.username}", category="success")
        return redirect(url_for("drinks_page"))
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
            return redirect(url_for("drinks_page"))
        else:
            flash("Username and Password are not match! Please try again!", category="danger")


    return render_template("login.html", form=form)

@app.route("/logout")
def logout_page():
    logout_user()
    flash("You have been logged out!", category="info")

    return redirect(url_for("home_page"))