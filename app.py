from flask import Flask, render_template , request , flash , session ,jsonify, make_response , redirect , url_for
from flask_sqlalchemy import SQLAlchemy
import json
from json import JSONEncoder

app = Flask(__name__)
app.secret_key = 'flasktutorial'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
db = SQLAlchemy(app)


users = ['ali','suliman','muhammed', 'bader' , 'saleh']
          #  0     1           2         3           4
# sql alchemy relationship one-one one-many many-many
# Table
class students(db.Model):
   __tablename__ = 'students'
   id = db.Column('student_id', db.Integer, primary_key = True)
   name = db.Column(db.String(100))
   city = db.Column(db.String(50))
   addr = db.Column(db.String(200))
   pin = db.Column(db.String(10))
   profile = db.relationship('Profile',uselist=False,backref='student')
   tasks = db.relationship('Tasks',uselist=True,backref='studenttask')

   def __init__(self, name, city, addr, pin):
       self.name = name
       self.city = city
       self.addr = addr
       self.pin = pin

class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column('profile_id', db.Integer, primary_key=True)
    class_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    student_id = db.Column(db.Integer,db.ForeignKey('students.student_id'))
class Tasks(db.Model):
    __tablename__ = 'tasks'
    id = db.Column('task_id', db.Integer, primary_key=True)
    task_name = db.Column(db.String(100))
    task_description = db.Column(db.String(100))
    task_duration = db.Column(db.String(100))
    task_place = db.Column(db.String(100))
    student_id = db.Column(db.Integer,db.ForeignKey('students.student_id'))



db.create_all()
# localhost:8000/
@app.route('/')
def index():
    return render_template('first.html' , users = users)
# localhost:8000/
@app.route('/about')
def about():
    return render_template('bader.html')
@app.route('/form', methods=['GET','POST'])
def form():

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        flash( "hello " + name)
        session['name'] = name
        session['age'] = age
        resp = make_response(render_template('post.html', Name = name , Age = age))
        resp.set_cookie('name',name)
        resp.set_cookie('age', age)
        return resp

    if 'name' in session:
        return render_template('post.html', Name = str(session['name']) , Age = str(session['age']))
    else:
        return render_template('form.html')
@app.route('/students-view')
def stdview():
    return render_template('table.html', students=students.query.all())
@app.route('/students', methods=['GET','POST'])
def students_index():
    if request.method == 'POST':
        name = request.form['name']
        city = request.form['city']
        addr = request.form['addr']
        pin = request.form['pin']
        student = students(name, city,addr, pin)
        db.session.add(student)
        db.session.commit()
        flash( "data added successfully ")
        return redirect(url_for('stdview'))
    return render_template('studentform.html')

@app.route('/students/edit/<student_id>', methods=['GET','POST'])
def edit_student(student_id):
    data = db.session.query(students).filter_by(id=student_id).one()
    if request.method == 'POST':
        name = request.form['name']
        city = request.form['city']
        addr = request.form['addr']
        pin = request.form['pin']
        data.name = name
        data.city = city
        data.addr = addr
        data.pin = pin
        db.session.commit()
        return redirect(url_for('stdview'))
    return render_template('edit.html', student = data)
@app.route('/students/delete/<student_id>')
def delete_student(student_id):
    db.session.query(students).filter_by(id=student_id).delete()
    db.session.commit()
    return redirect(url_for('stdview'))
@app.route('/students/add/<student_id>',methods=['GET','POST'])
def add_info(student_id):
    student = db.session.query(students).filter_by(id=student_id).one()
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        profile = Profile(class_name = name, age = age , student = student)
        db.session.add(profile)
        db.session.commit()
        flash("data added successfully ")
        return redirect(url_for('stdview'))
    return render_template('profile.html',id= student_id)
@app.route('/students/show/<student_id>')
def show_info(student_id):
    data = db.session.query(students).filter_by(id=student_id).one()
    return  render_template('show.html',data= data)
@app.route('/students/addtask/<student_id>',methods=['GET','POST'])
def add_task(student_id):
    student = db.session.query(students).filter_by(id=student_id).one()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        duration = request.form['duration']
        place = request.form['place']
        task = Tasks(task_name = name, task_description = description, task_duration = duration, task_place = place , studenttask = student)
        db.session.add(task)
        db.session.commit()
        flash("data added successfully ")
        return redirect(url_for('stdview'))
    return render_template('taskform.html')
@app.route('/students/showtask/<student_id>')
def show_tasks(student_id):
    data = db.session.query(students).filter_by(id=student_id).one()
    return  render_template('show2.html',data= data)
if __name__ == '__main__':
    app.run(port=3000,debug=True)