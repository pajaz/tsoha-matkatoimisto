from application import app, db
from flask import redirect, render_template, request, url_for
from application.matkakohteet.models import Matkakohde


@app.route("/matkakohteet/", methods=["GET"])
def matkakohteet_index():
    return render_template("matkakohteet/list.html", matkakohteet = Matkakohde.query.all())


@app.route("/matkakohteet/uusi")
def matkakohteet_form():
    return render_template("matkakohteet/new.html")

@app.route("/matkakohteet/", methods=["POST"])
def matkakohteet_create():

    dest_name = request.form.get("name")
    dest_country = request.form.get("country")
    dest = Matkakohde(dest_name.title(), dest_country.title())

    db.session().add(dest)
    db.session().commit()

    return redirect(url_for("matkakohteet_index"))

@app.route('/matkakohteet/edit/<int:id>', methods=['GET'])
def matkakohteet_edit_form(id):
    
    destination = Matkakohde.query.get_or_404(id)  
    return render_template("matkakohteet/matkakohde.html", matkakohde = destination, id = destination.id)

@app.route("/matkakohteet/edit/<matkakohde_id>", methods=["POST"])
def matkakohteet_edit(matkakohde_id):
    
    dest_name = request.form.get("name")
    dest_country = request.form.get("country")
    dest_intro = request.form.get("intro")

    destination = Matkakohde.query.get_or_404(matkakohde_id)

    destination.name = dest_name
    destination.country = dest_country
    destination.intro = dest_intro

    db.session().commit()

    return redirect(url_for("matkakohteet_index"))

@app.route("/matkakohteet/delete/<int:id>", methods=["GET"])
def matkakohteet_delete(id):

    destination = Matkakohde.query.get_or_404(id)

    db.session.delete(destination)
    db.session.commit()

    return redirect(url_for("matkakohteet_index"))