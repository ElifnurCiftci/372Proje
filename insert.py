from queries import insert

for i in range(4):
    name = "Movie {}".format(i)
    image = "movie{}.png".format(i)
    insert(table="movie",columns= "name,image",values="'{}','{}'".format(name,image))
for i in range(4):
    name = "Actor {}".format(i)
    image = "actor{}.png".format(i)
    insert(table="actor",columns= "name,image",values="'{}','{}'".format(name,image))

insert("index", "movie_id,actor_id","1,1")
insert("index", "movie_id,actor_id","1,3")
insert("index", "movie_id,actor_id","1,4")
insert("index", "movie_id,actor_id","2,3")
insert("index", "movie_id,actor_id","2,4")
insert("index", "movie_id,actor_id","2,1")
insert("index", "movie_id,actor_id","3,4")
insert("index", "movie_id,actor_id","3,3")
insert("index", "movie_id,actor_id","4,4")
insert("index", "movie_id,actor_id","4,1")
