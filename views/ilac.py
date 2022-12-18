from flask import Blueprint, request, render_template, redirect, url_for
from queries import *

ilac = Blueprint("ilac",import_name=__name__, template_folder="templates")

@ilac.route("/", methods=['GET','POST'])
def ilac_page():
    if request.method == "GET":
        ilac = select("ilac_adi,ilac_cesidi,ilac_id,son_kullanma_tarihi","ilac order by son_kullanma_tarihi asc",asDict=True)
        return render_template("ilac.html", ilac = ilac)