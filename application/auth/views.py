from flask import redirect, render_template, request, url_for
from flask_login import login_user, logout_user

from application import app, db
from application.auth.models import Kayttaja
from application.auth.forms import LoginForm, NewUserForm

@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    form = LoginForm(request.form)

    #Tähän validointeja

    username = form.username.data
    password = form.password.data

    user = Kayttaja.query.filter_by(username=username, password=password).first()
    if not user:
        return render_template("auth/loginform.html", form = form, 
                                error = "Tuntematon käyttäjänimi tai salasana")
    
    login_user(user)
    return redirect(url_for("matkakohteet_index"))

@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/auth/new", methods = ["GET", "POST"])
def auth_new():
    if request.method == "GET":
        return render_template("auth/newuserform.html", form = NewUserForm())

    form = NewUserForm(request.form)

    if request.method == 'POST' and form.validate():

        first_name = form.firstname.data
        last_name = form.lastname.data
        phone = form.phone_number.data
        email = form.email.data
        username = form.username.data
        pword = form.password.data

        if not email:
            user = Kayttaja(first_name.title(), last_name.title(), username, phone, pword)
        else:
            user = Kayttaja(first_name.title(), last_name.title(), username, phone, pword, email)

        db.session().add(user)
        db.session().commit()

        return redirect(url_for("index"))
    return render_template("auth/newuserform.html", form = form)