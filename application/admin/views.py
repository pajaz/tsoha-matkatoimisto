from application import app, db
from flask import redirect, render_template, request, url_for
from application.models import Matkakohde
from application.admin.forms import DestinationForm


@app.route("/matkakohteet/", methods=["GET"])
def matkakohteet_index():
    return render_template("admin/list.html", matkakohteet = Matkakohde.query.all())


@app.route("/matkakohteet/uusi")
def matkakohteet_form():
    return render_template("admin/new.html", form = DestinationForm())

@app.route("/matkakohteet/", methods=["POST"])
def matkakohteet_create():

    form = DestinationForm(request.form)

    dest_name = form.name.data
    dest_country = form.country.data
    dest_intro = form.description.data
    if not dest_intro:
        dest = Matkakohde(dest_name.title(), dest_country.title())
    else:
        dest = Matkakohde(dest_name.title(), dest_country.title(), dest_intro)

    db.session().add(dest)
    db.session().commit()

    return redirect(url_for("matkakohteet_index"))

@app.route('/matkakohteet/edit/<int:id>', methods=['GET'])
def matkakohteet_edit_form(id):
    
    destination = Matkakohde.query.get_or_404(id)  
    return render_template("admin/matkakohde.html", form = DestinationForm(), matkakohde = destination, id = destination.id)

@app.route("/matkakohteet/edit/<matkakohde_id>", methods=["POST"])
def matkakohteet_edit(matkakohde_id):
    
    form = DestinationForm(request.form)

    dest_name = form.name.data
    dest_country = form.country.data
    dest_intro = form.description.data

    destination = Matkakohde.query.get_or_404(matkakohde_id)

    destination.name = dest_name
    destination.country = dest_country
    destination.intro = dest_intro

    db.session().commit()

    return redirect(url_for("matkakohteet_index"))

@app.route("/matkakohteet/delete/<matkakohde_id>", methods=["GET", "POST"])
def matkakohteet_delete(matkakohde_id):

    destination = Matkakohde.query.get_or_404(matkakohde_id)
    print("ABOUT TO DELETE!!!!" + str(destination.id) + "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    
    db.session.delete(destination)
    db.session.commit()

    return redirect(url_for("matkakohteet_index"))