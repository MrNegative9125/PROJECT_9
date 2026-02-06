from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employee.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Employees(db.Model):
    __tablename__ = "employees"   # ✅ explicit table name

    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(500), nullable=False)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        employee = Employees(name=name, email=email)
        db.session.add(employee)
        db.session.commit()

        return redirect("/")  # ✅ prevents duplicate insert on refresh

    allemployees = Employees.query.all()
    return render_template('index.html', allemployees=allemployees)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route("/delete/<int:sno>")
def delete(sno):
    employee = Employees.query.get(sno)
    if employee:
        db.session.delete(employee)
        db.session.commit()
    return redirect("/")


@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    employee = Employees.query.get(sno)

    if request.method == 'POST':
        employee.name = request.form['name']
        employee.email = request.form['email']
        db.session.commit()
        return redirect("/")

    return render_template("update.html", employee=employee)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()   # ✅ creates table if not exists
    app.run(debug=True)
