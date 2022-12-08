from flask import Blueprint, request, render_template, redirect, url_for
from queries import *

eczane = Blueprint("eczane",import_name=__name__, template_folder="templates")

@eczane.route("/", methods=['GET','POST'])
def eczane_page():
    if request.method == "GET":
        eczane = select("eczane_ad,eczane_id,eczane_adres,eczane_tel_no,eczane_e_posta","eczane",asDict=True)
        return render_template("eczane.html", eczane = eczane)
    """ elif request.method == "POST":
        if "like" in request.form:
            update("eczane","likes=likes+1","id={}".format(request.form.get('like')))
        elif "dislike" in request.form:
            update("eczane","dislikes=dislikes+1","id={}".format(request.form.get('dislike')))
        return redirect(url_for('eczane.eczane_page')) """

@eczane.route("/<eczane_id>")
def eczane_detail_page(eczane_id):
    ilac = select("ilac_adi,ilac_id","ilac natural join anlasma_saglar","eczane_id='{}'".format(eczane_id),asDict=True)
    eczane_ad = select("eczane_ad","eczane","eczane_id='{}'".format(eczane_id),asDict=True)
    return render_template("eczane_detail_page.html", ilac = ilac, eczane_ad=eczane_ad)