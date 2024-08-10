from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm, StudentDetailsForm, CourseRegistrationForm, FinanceForm, DemographicForm
from app.models import User, Student, Course, Registration, Finance, Demographic

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/my_academics')
@login_required
def my_academics():
    student = Student.query.filter_by(user_id=current_user.id).first()
    return render_template('my_academics.html', student=student)

@app.route('/specialization', methods=['GET', 'POST'])
@login_required
def specialization():
    student = Student.query.filter_by(user_id=current_user.id).first()
    form = StudentDetailsForm(obj=student)
    if form.validate_on_submit():
        form.populate_obj(student)
        db.session.commit()
        flash('Specialization updated successfully!')
        return redirect(url_for('my_academics'))
    return render_template('specialization.html', form=form)

@app.route('/registration', methods=['GET', 'POST'])
@login_required
def registration():
    form = CourseRegistrationForm()
    if form.validate_on_submit():
        registration = Registration(student_id=current_user.id, course_id=form.course_id.data, semester=form.semester.data)
        db.session.add(registration)
        db.session.commit()
        flash('Course registered successfully!')
        return redirect(url_for('my_academics'))
    return render_template('registration.html', form=form)

@app.route('/my_finance', methods=['GET', 'POST'])
@login_required
def my_finance():
    finance = Finance.query.filter_by(student_id=current_user.id).first()
    form = FinanceForm(obj=finance)
    if form.validate_on_submit():
        form.populate_obj(finance)
        db.session.commit()
        flash('Finance details updated successfully!')
        return redirect(url_for('my_finance'))
    return render_template('my_finance.html', form=form)

@app.route('/demographic_details', methods=['GET', 'POST'])
@login_required
def demographic_details():
    demographic = Demographic.query.filter_by(student_id=current_user.id).first()
    form = DemographicForm(obj=demographic)
    if form.validate_on_submit():
        form.populate_obj(demographic)
        db.session.commit()
        flash('Demographic details updated successfully!')
        return redirect(url_for('demographic_details'))
    return render_template('demographic_details.html', form=form)

@app.route('/student_center')
@login_required
def student_center():
    student = Student.query.filter_by(user_id=current_user.id).first()
    return render_template('student_center.html', student=student)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
