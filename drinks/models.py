from drinks import db, login_manager
from drinks import bcrypt
from flask_login import UserMixin
#import RPi.GPIO as GPIO
import time

#GPIO.setmode(GPIO.BCM)
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
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

class Drink(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False)
    mapping = db.relationship("Map", backref="drink", lazy=True)
    
    def __repr__(self):
        return f'Drink {self.id}, {self.name}, {self.description}'

    # def mix_drink(self):
       # ingList = db.session.query(Ingredient.pump, Ingredient.name, Map.ratio).filter(Map.drinkID==self.id).filter(Ingredient.id==Map.ingredientID).all()
       # for ing in ingList:
       #     GPIO.setup(ing[0], GPIO.OUT)

       # for ing in ingList:
       #     max_ml = GLAS * ing[2] / 100 # 100 ml von 300 ml
       #     waitTime = max_ml / FLOW_RATE
       #     GPIO.output(ing[0], GPIO.LOW)
       #     time.sleep(waitTime)
       #     GPIO.output(ing[0], GPIO.HIGH)
    
    # def wash_machine(self):
        # for ing in ingList:
        #     GPIO.setup(ing[0], GPIO.OUT)

        # pumpList = ['17', '27', '22']
        # for p in pumplist:
        #     max_ml = 100
        #     waitTime = max_ml / FLOW_RATE
        #     GPIO.output(p, GPIO.LOW)
        #     time.sleep(waitTime)
        #     GPIO.output(p, GPIO.HIGH)

class Ingredient(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
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