from flask import Blueprint, request, render_template, redirect, url_for
from queries import *

actor = Blueprint("actor",import_name=__name__, template_folder="templates")

@actor.route("/", methods=['GET','POST'])
def actors_page():
    if request.method == "GET":
        actors = select("id,name,likes,dislikes,image","actor",asDict=True)
        return render_template("actors.html", actors = actors)
    elif request.method == "POST":
        if "like" in request.form:
            update("actor","likes=likes+1","id={}".format(request.form.get('like')))
        elif "dislike" in request.form:
            update("actor","dislikes=dislikes+1","id={}".format(request.form.get('dislike')))
        return redirect(url_for('actor.actors_page'))

@actor.route("/<id>")
def actor_detail_page(id):
    actor = select("name,image","movie","id={}".format(id),asDict=True)
    movies = select("movie.name, movie.likes, movie.dislikes, movie.image",
    "movie join index on movie.id=index.movie_id","index.actor_id={}".format(id), asDict=True)
    return render_template("actor_detail_page.html", movies=movies, actor=actor)