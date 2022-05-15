from wtforms import StringField, validators, Form

class Addproducts(Form):
    name = StringField('Name', [validators.DataRequired()])
    