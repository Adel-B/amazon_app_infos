from flask_wtf import Form 
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL

class search_form(Form):
  url = StringField('Application URL', validators=[DataRequired("Please enter an App’s Amazon Store URL"), URL("Please enter an App’s Amazon Store URL")])
  submit = SubmitField("Get infos about this application ")

