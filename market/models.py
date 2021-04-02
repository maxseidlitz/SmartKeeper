from market import db, login_manager
from market import bcrypt
from flask_login import UserMixin
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
FLOW_RATE = 125/60
MAX_TIME = 0
GLAS = 300

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)

    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}$'
        else:
            return f'{self.budget}$'

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
    
    def can_purchase(self, drink_obj):
        return True #self.budget >= item_obj.price

    # def can_sell(self, sell_obj):
    #     return sell_obj in self.items

# class Item(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(length=30), nullable=False, unique=True)
#     price = db.Column(db.Integer(), nullable=False)
#     barcode = db.Column(db.String(length=12), nullable=False, unique=True)
#     description = db.Column(db.String(length=1024), nullable=False, unique=True)
#     owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

#     def __repr__(self):
#         return f'Item {self.name}'

#     def buy(self, user):
#         self.owner = user.id
#         user.budget -= self.price
#         db.session.commit()

#     def sell(self, user):
#         self.owner = None
#         user.budget += self.price
#         db.session.commit()

class Drink(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False)
    mapping = db.relationship("Map", backref="drink", lazy=True)
    
    def __repr__(self):
        return f'Drink {self.id}, {self.name}, {self.description}'

    def mix_drink(self):
        ingList = db.session.query(Ingredient.pump, Ingredient.name, Map.ratio).filter(Map.drinkID==self.id).filter(Ingredient.id==Map.ingredientID).all()
        print(ingList)
        for ing in ingList:
            GPIO.setup(ing[0], GPIO.OUT)

        for ing in ingList:
            max_ml = GLAS * ing[2] / 100 # 100 ml von 300 ml
            waitTime = max_ml / FLOW_RATE
            GPIO.output(ing[0], GPIO.LOW)
            time.sleep(waitTime)
            GPIO.output(ing[0], GPIO.HIGH)
        
class Ingredient(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False)
    percentage = db.Column(db.Integer(), nullable=False)
    pump = db.Column(db.Integer(), nullable=False)
    mapping = db.relationship("Map", backref="ingredient", lazy=True)

    def __repr__(self):
        return f'Ingredient {self.id}, {self.name}, {self.percentage}, {self.pump}'

class Map(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    ratio = db.Column(db.Integer(), nullable=False)
    drinkID = db.Column(db.Integer(), db.ForeignKey('drink.id'), nullable=False)
    ingredientID = db.Column(db.Integer(), db.ForeignKey('ingredient.id'), nullable=False)

    def __repr__(self):
        return f'Map {self.id}, {self.ratio}, {self.drinkID}, {self.ingredientID}'