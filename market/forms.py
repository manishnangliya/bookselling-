from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField, IntegerField
from wtforms.validators import Length, Email, EqualTo, DataRequired, ValidationError
from market.models import User

class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exist!')
        
    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exist!')

    username = StringField(label='User Name', validators=[Length(min=4, max=30), DataRequired()])
    email_address = StringField(label='Email', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    username = StringField(label='User Name', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase Items!')
    
class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell Items!')

class AddItemsForm(FlaskForm):
    name = StringField(label='name', validators=[ DataRequired()])
    price = IntegerField(label='price', validators=[DataRequired()])
    barcode = StringField(label='barcode', validators=[ DataRequired()])
    description = StringField(label='description', validators=[Length( max=1024), DataRequired()])
    submit = SubmitField(label='Add Item')
    
