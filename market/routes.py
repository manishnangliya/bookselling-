# import re
# import flask_sqlalchemy
from market import app
from flask import render_template, redirect, url_for, flash, request
from .models import Item, User
from .forms import AddItemsForm, RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
def home():
    return render_template('home.html')

@app.route("/sell", methods=['GET', 'POST'])
@login_required
def sell_view():
    sell = AddItemsForm()
    if request.method == 'POST':
        if sell.validate_on_submit():
            user_to_sell = Item(name=sell.name.data,
                            price=sell.price.data,
                            barcode=sell.barcode.data,
                            description=sell.description.data)
            db.session.add(user_to_sell)
            db.session.commit()
            user_to_sell.sell(current_user)
            flash( f'Item successfully sold:', category='success')
            return redirect(url_for('market'))
        if sell.errors != {}: #If there are not errors from the validations
            for err_msg in sell.errors.values():
                flash(f'Error: {err_msg}', category='danger')

    return render_template('sell.html', sell =sell)

@app.route("/market", methods=['GET', 'POST'])
@login_required
def market():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    if request.method =='POST':
        #purchase item logic
        purchased_item = request.form.get('purchased_item')
        if purchased_item:
            p_item_object = Item.query.filter_by(name=purchased_item).first()
            if p_item_object:
                if current_user.can_purchase(p_item_object): #execution code in models as buy function
                    p_item_object.buy(current_user)
                    # p_item_object.owner = current_user.id
                    # current_user.budget -= p_item_object.price
                    # db.session.commit()
                    flash(f"Congratulation: You puchased {p_item_object.name} for Rs.{p_item_object.price}",category='success')
                
                else:
                    flash(f"Unfortunetely, you don't have enough money to purchase {p_item_object.name}", category='danger')
        #sell item logic
        else:
            sold_item = request.form.get('sold_item')
            s_item_object = Item.query.filter_by(name=sold_item).first()
            if s_item_object:
                if current_user.can_sell(s_item_object):
                    s_item_object.sell(current_user)
                    flash(f"Congratulation: You Sold  {s_item_object.name} back to market! ",category='success')
                else:
                    flash(f"Something went wrong with selling {s_item_object.name}" ,category='danger')

                return redirect(url_for('market'))
        return redirect(url_for('market'))       
    # if purchase_form.validate_on_submit():
        # print(purchase_form.__dict__)
        # print(purchase_form['submit'])
        # print(purchase_form['purchased_item']) ///not working
        
    # items = Item.query.all()
    if request.method=='GET': ##to remove default conformation method use get and post method
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items = items, purchase_form=purchase_form,owned_items=owned_items,selling_form=selling_form)

@app.route("/register", methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user_to_create = User(username=form.username.data,
                            email_address=form.email_address.data,
                            password=form.password1.data)
            db.session.add(user_to_create)
            db.session.commit()
            flash( f'You have successfully Registered as username:', category='success')
            return redirect(url_for('login_page'))
        if form.errors != {}: #If there are not errors from the validations
            for err_msg in form.errors.values():
                flash(f'Error: {err_msg}', category='danger')

    return render_template("register.html", form = form)

@app.route("/login", methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            attempted_user = User.query.filter_by(username=form.username.data).first()
            if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
                login_user(attempted_user)
                flash( f'Successfuly logged in as: { attempted_user.username }', category='success')
                return redirect( url_for('market'))
            else:
                flash('Username and password are wrong ! please try again', category='danger')

    return render_template("login.html", form = form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out", category='info')
    return redirect(url_for("home"))