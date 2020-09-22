insert into movie (name,image) values('Movie 1','movie1.png');
insert into movie (name,image) values('Movie 2','movie2.png');
insert into movie (name,image) values('Movie 3','movie3.png');
insert into movie (name,image) values('Movie 4','movie4.png');

insert into actor (name,image) values('Actor 1','actor1.png');
insert into actor (name,image) values('Actor 2','actor2.png');
insert into actor (name,image) values('Actor 3','actor3.png');
insert into actor (name,image) values('Actor 4','actor4.png');

insert into index (movie_id,actor_id) values(1,1);
insert into index (movie_id,actor_id) values(1,3);
insert into index (movie_id,actor_id) values(1,4);
insert into index (movie_id,actor_id) values(2,3);
insert into index (movie_id,actor_id) values(2,4);
insert into index (movie_id,actor_id) values(2,1);
insert into index (movie_id,actor_id) values(3,4);
insert into index (movie_id,actor_id) values(3,3);
insert into index (movie_id,actor_id) values(4,4);
insert into index (movie_id,actor_id) values(4,1);