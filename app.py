# app.py (with pagination added)
from flask import Flask, render_template, redirect, url_for, session, request, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm, StudentForm
from generate_pdf import create_pdf
from math import ceil

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
db = SQLAlchemy(app)

from models import Admin, Student

# ✅ Initialize tables and admin
with app.app_context():
    db.create_all()
    if not Admin.query.first():
        admin = Admin(username='admin', password='admin123')
        db.session.add(admin)
        db.session.commit()


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin and admin.password == form.password.data:
            session['admin'] = admin.username
            return redirect(url_for('dashboard'))
        flash('Invalid credentials')
    return render_template('login.html', form=form)

@app.route('/dashboard')
def dashboard():
    if 'admin' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if 'admin' not in session:
        return redirect(url_for('login'))
    form = StudentForm()
    if form.validate_on_submit():
        total = form.subject1.data + form.subject2.data + form.subject3.data + form.subject4.data + form.subject5.data
        average = total / 5
        if average >= 90:
            grade = 'A'
        elif average >= 75:
            grade = 'B'
        elif average >= 60:
            grade = 'C'
        elif average >= 45:
            grade = 'D'
        else:
            grade = 'F'
        student = Student(
            name=form.name.data,
            roll_no=form.roll_no.data,
            subject1=form.subject1.data,
            subject2=form.subject2.data,
            subject3=form.subject3.data,
            subject4=form.subject4.data,
            subject5=form.subject5.data,
            total=total,
            average=average,
            grade=grade
        )
        db.session.add(student)
        db.session.commit()
        flash('Student added successfully')
        return redirect(url_for('view_students'))
    return render_template('add_student.html', form=form)

@app.route('/students')
def view_students():
    if 'admin' not in session:
        return redirect(url_for('login'))
    query = request.args.get('q')
    page = request.args.get('page', 1, type=int)
    per_page = 5

    if query:
        students = Student.query.filter(
            (Student.name.contains(query)) | (Student.roll_no.contains(query))
        ).paginate(page=page, per_page=per_page)
    else:
        students = Student.query.paginate(page=page, per_page=per_page)
    return render_template('view_students.html', students=students)

@app.route('/report/<int:id>')
def generate_report(id):
    if 'admin' not in session:
        return redirect(url_for('login'))
    student = Student.query.get_or_404(id)
    pdf = create_pdf(student)
    return send_file(pdf, as_attachment=True, download_name='report.pdf', mimetype='application/pdf')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    if 'admin' not in session:
        return redirect(url_for('login'))
    student = Student.query.get_or_404(id)
    form = StudentForm(obj=student)
    if form.validate_on_submit():
        student.name = form.name.data
        student.subject1 = form.subject1.data
        student.subject2 = form.subject2.data
        student.subject3 = form.subject3.data
        student.subject4 = form.subject4.data
        student.subject5 = form.subject5.data
        student.total = student.subject1 + student.subject2 + student.subject3 + student.subject4 + student.subject5
        student.average = student.total / 5
        if student.average >= 90:
            student.grade = 'A'
        elif student.average >= 75:
            student.grade = 'B'
        elif student.average >= 60:
            student.grade = 'C'
        elif student.average >= 45:
            student.grade = 'D'
        else:
            student.grade = 'F'
        db.session.commit()
        flash('Student record updated')
        return redirect(url_for('view_students'))
    return render_template('edit_student.html', form=form)

@app.route('/delete/<int:id>')
def delete_student(id):
    if 'admin' not in session:
        return redirect(url_for('login'))
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash('Student record deleted')
    return redirect(url_for('view_students'))


@app.route('/student/<roll_no>')
def student_public_view(roll_no):
    student = Student.query.filter_by(roll_no=roll_no).first()
    if not student:
        return "<h3>Student not found.</h3>", 404
    return render_template('student_view.html', student=student)
 

if __name__ == '__main__':
    app.run(debug=True)
