from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField, SelectField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError, NumberRange
from sqlalchemy import asc
from drinks import db
from drinks.models import User, Ingredient

class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username.')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different Email Address')

    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit_CreateAcc = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = StringField(label='Password:', validators=[DataRequired()])
    submit_LogIn = SubmitField(label='Sign In')

class MixDrinkForm(FlaskForm):
    submit_MixDrink = SubmitField(label='MIX IT!')

class AddDrinkForm(FlaskForm):
    name = StringField(label='Name:', validators=[Length(min=2, max=30), DataRequired()])
    description = TextAreaField(label='Description:', validators=[Length(min=2, max=1024), DataRequired()])

    ingredientChoice_1 = SelectField(u'Ingredient 1', coerce=str, validators=[DataRequired()]) 
    ratio_1 = IntegerField(label='Ratio 1:', validators=[NumberRange(min=0, max=3), DataRequired()])
    ingredientChoice_2 = SelectField(u'Ingredient 2', coerce=str, validators=[DataRequired()])
    ratio_2 = IntegerField(label='Ratio 2:', validators=[NumberRange(min=0, max=3)])
    ingredientChoice_3 = SelectField(u'Ingredient 3', coerce=str, validators=[DataRequired()])
    ratio_3 = IntegerField(label='Ratio 3:', validators=[NumberRange(min=0, max=3)])
    submit_AddDrink = SubmitField(label='Add Drink')

class AddIngredientForm(FlaskForm):
    name = StringField(label='Name:', validators=[Length(min=2, max=30), DataRequired()])
    percentage = IntegerField(label='Alcohol Percentage:', validators=[NumberRange(min=0, max=3), DataRequired()])
    pump = SelectField(label='Pump:', choices=['17', '27', '22', '23', '24', '25', '5', '6', '16', '26'], validators=[DataRequired()])
    submit_AddIngredient = SubmitField(label='Add Ingredient')

class DeleteDrinkForm(FlaskForm):
    name = StringField(label='Name:', validators=[Length(min=2, max=30), DataRequired()])
    submit_DeleteDrink = SubmitField(label='Delete')