from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "mydatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    expensename = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)


@app.route("/")
def add():
    return render_template("add.html")

@app.route("/addexpense", methods=["POST"])
def addexpense():
    date = request.form["date"]
    expensename = request.form["expensename"]
    amount = request.form["amount"]
    category = request.form["category"]
    print(date+" "+expensename+" "+amount+" "+category)
    expense = Expense(
        date=date, expensename=expensename, amount=amount, category=category
    )
    db.session.add(expense)
    db.session.commit()
    return redirect("/expenses")

@app.route("/updateexpense/<int:id>")
def updateexpense(id):
    expense = Expense.query.filter_by(id=id).first()
    return render_template("updateexpense.html", expense=expense)

@app.route("/edit", methods=['POST'])
def edit():
    id = request.form["id"]
    date = request.form["date"]
    expensename = request.form["expensename"]
    amount = request.form["amount"]
    category = request.form["category"]

    expense = Expense.query.filter_by(id=id).first()
    expense.date = date
    expense.expensename = expensename
    expense.amount = amount
    expense.category = category

    db.session.commit()
    return redirect("/expenses")

@app.route("/delete/<int:id>")
def delete(id):
    expense = Expense.query.filter_by(id=id).first()
    db.session.delete(expense)
    db.session.commit()
    return redirect("/expenses")

@app.route("/expenses")
def expenses():
    expenses = Expense.query.all()
    total = 0
    t_rent = 0
    t_food = 0
    t_commute = 0
    t_misc = 0
    for expense in expenses:
        total += expense.amount
        if expense.category == "rent":
            t_rent += expense.amount
        elif expense.category == "food":
            t_food += expense.amount
        elif expense.category == "commute":
            t_commute += expense.amount
        elif expense.category == "misc":
            t_misc += expense.amount
    return render_template("expenses.html", expenses=expenses, total=total, t_misc=t_misc, t_food=t_food, t_rent=t_rent, t_commute=t_commute)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
