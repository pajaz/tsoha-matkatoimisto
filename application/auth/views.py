# application/auth/views.py
from flask import redirect, render_template, request, url_for
from flask_login import login_user, logout_user, login_required

from math import ceil
from application import app, db, login_required
from application.auth.models import Kayttaja, Role, roles
from application.auth.forms import LoginForm, NewUserForm
from application.varaukset.models import Varaus

# Kirjautumislomakkeen haku, sekä lähetys
@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())
    
    form = LoginForm(request.form)

    if form.validate():
        username = form.username.data
        password = form.password.data

        user = Kayttaja.query.filter_by(username=username, password=password).first()
        if not user:
            return render_template("auth/loginform.html", form = form, 
                                error = "Tuntematon käyttäjänimi tai salasana")
    
        login_user(user)
        return redirect(url_for("matkakohteet_index"))
    return render_template("auth/loginform.html", form = form)

    
# Uloskirjaus
@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))

# Uuden käyttäjän luomiseen käytettävän lomakkeen haku ja lähetys
@app.route("/auth/new", methods = ["GET", "POST"])
def auth_new():
    if request.method == "GET":
        return render_template("auth/newuserform.html", form = NewUserForm(), add_user=True)
    form = NewUserForm(request.form)

    if request.method == 'POST' and form.validate():

        first_name = form.first_name.data
        last_name = form.last_name.data
        phone = form.phone_number.data
        email = form.email.data
        username = form.username.data
        pword = form.password.data
        admin = form.admin.data
        
        print(admin)

        if not email:
            user = Kayttaja(first_name.title(), last_name.title(), username, phone, pword, admin)
        else:
            user = Kayttaja(first_name.title(), last_name.title(), username, phone, pword, admin, email)


        db.session().add(user)
        db.session.flush()
        if admin == 1:
           adminrole = roles.insert().values(role_id = 1, kayttaja_id = user.id)
           db.session.execute(adminrole)
        
        user_role = roles.insert().values(role_id = 2, kayttaja_id = user.id)
        db.session.execute(user_role)
        db.session().commit()

        return redirect(url_for("index"))
    return render_template("auth/newuserform.html", form = form, add_user=True)

# Käyttäjätietonäkymä
@app.route("/auth/<user_id>", methods=["GET"])
@login_required(role="User")
def user_info(user_id):
    kayttaja = Kayttaja.query.get_or_404(user_id)
    bookings = kayttaja.get_booking_infos()
    for b in bookings:
        print(type(b))
        print(b)
    return render_template("auth/user_info.html", kayttaja = kayttaja, varaukset=bookings)

# Käyttäjän muokkaus
@app.route("/auth/edit/<user_id>", methods=["GET", "POST"])
@login_required(role="User")
def edit_user(user_id):


    kayttaja = Kayttaja.query.get_or_404(user_id)
    form = NewUserForm(obj=kayttaja)
    bookings = kayttaja.get_booking_infos()
    

    if request.method == "POST" and form.validate():
        kayttaja.first_name = form.first_name.data
        kayttaja.last_name = form.last_name.data
        kayttaja.phone_number = form.phone_number.data
        kayttaja.email = form.email.data
        kayttaja.username = form.username.data
        kayttaja.password = form.password.data
        kayttaja.admin = form.admin.data

        db.session().commit()

        return redirect(url_for("user_info", user_id=user_id))

    return render_template("auth/newuserform.html", form=form, kayttaja=kayttaja, user_id=user_id,
                           varaukset=bookings, add_user=False)

# Käyttäjälistaus ja haku 
@app.route("/kayttajat/", methods=["GET"])
@login_required(role="Admin")
def kayttajat_index():
    orderby = request.args.get("order", "id", type=str)
    page = request.args.get("page", 1, type=int)
    show = 6 
    
    users = Kayttaja.query.order_by(orderby, "id").paginate(page, show, False).items
    bookings = [len(nmbr.get_booking_infos()) for nmbr in users]
    user_bookings = zip(users, bookings)
    pages = ceil(Kayttaja.query.count()/show)

    return render_template("auth/list.html", kayttajat=user_bookings, varaukset=bookings, page=page, pages=pages, order=orderby)

# Delete dem users
@app.route("/auth/delete/<user_id>", methods=["GET","POST"])
@login_required(role="Admin")
def kayttaja_delete(user_id):
    
    user = Kayttaja.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect(url_for("kayttajat_index"))