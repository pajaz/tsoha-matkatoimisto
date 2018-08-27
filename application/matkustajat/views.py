# application/matkustajat/views.py
from flask import redirect, render_template, request, url_for
from flask_login import login_required

from application import app, db, login_required
from application.matkustajat.models import Matkustaja
from application.varaukset.models import matkustaja_varaus
from application.varaukset.models import Varaus

@app.route("/matkustajat/delete_from_booking/<matkustaja_id>", methods=["GET", "POST"])
def delete_matkustaja(matkustaja_id):
    print(matkustaja_id)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    previous_page = request.args.get("previous_page")
    varaus_id = request.args.get("varaus_id")

    varaus = Varaus.query.get_or_404(varaus_id)

    varaus.delete_passenger_from_booking(matkustaja_id)


    return redirect(url_for(previous_page, varaus_id = varaus_id))