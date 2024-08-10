from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, FloatField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User, Student, Course

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class StudentDetailsForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    major = StringField('Major', validators=[DataRequired()])
    academic_year = StringField('Academic Year', validators=[DataRequired()])
    specialization_id = SelectField('Specialization', coerce=int)
    submit = SubmitField('Update')

    def __init__(self, *args, **kwargs):
        super(StudentDetailsForm, self).__init__(*args, **kwargs)
        self.specialization_id.choices = [(s.id, s.name) for s in Specialization.query.all()]

class CourseRegistrationForm(FlaskForm):
    course_id = SelectField('Course', coerce=int)
    semester = StringField('Semester', validators=[DataRequired()])
    submit = SubmitField('Register')

    def __init__(self, *args, **kwargs):
        super(CourseRegistrationForm, self).__init__(*args, **kwargs)
        self.course_id.choices = [(c.id, c.name) for c in Course.query.all()]

class FinanceForm(FlaskForm):
    tuition_fee = FloatField('Tuition Fee', validators=[DataRequired()])
    payment_status = StringField('Payment Status', validators=[DataRequired()])
    submit = SubmitField('Update Finance Details')

class DemographicForm(FlaskForm):
    address = TextAreaField('Address', validators=[DataRequired(), Length(min=10, max=255)])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=15)])
    emergency_contact = StringField('Emergency Contact', validators=[DataRequired()])
    submit = SubmitField('Update Demographic Details')
