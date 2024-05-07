from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, URL

class CrawlForm(FlaskForm):
    start_url = StringField('Start URL', validators=[DataRequired(), URL()])
    output_dir = StringField('Output Directory', default='URLs')
    max_workers = IntegerField('Maximum Workers', default=10)
    submit = SubmitField('Start Crawling')

class CompareForm(FlaskForm):
    archive_folder = StringField('Archive Folder Path', validators=[DataRequired()])
    submit = SubmitField('Compare Archives')
