from flask import Blueprint, request, render_template, redirect, url_for
from queries import *

movie = Blueprint("movie",import_name=__name__, template_folder="templates")

@movie.route("/", methods=['GET','POST'])
def movies_page():
    if request.method == "GET":
        movies = select("id,name,likes,dislikes,image","movie",asDict=True)
        return render_template("movies.html", movies = movies)
    elif request.method == "POST":
        if "like" in request.form:
            update("movie","likes=likes+1","id={}".format(request.form.get('like')))
        elif "dislike" in request.form:
            update("movie","dislikes=dislikes+1","id={}".format(request.form.get('dislike')))
        return redirect(url_for('movie.movies_page'))

@movie.route("/<id>")
def movie_detail_page(id):
    movie = select("name,image","movie","id={}".format(id),asDict=True)
    actors = select("actor.name, actor.likes, actor.dislikes, actor.image",
    "actor join index on actor.id=index.actor_id","index.movie_id={}".format(id), asDict=True)
    return render_template("movie_detail_page.html", movie=movie, actors=actors)