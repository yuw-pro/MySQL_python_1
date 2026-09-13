create  database if not exists douban;
use douban; 
create table if not exists douban_films(
    rank_no int primary key auto_increment,
    title varchar(255) not null,
    director varchar(255),
    actors varchar(255),
    genre varchar(255),
    release_date date,

    rating float,
    review_count int,
    film_url varchar(255)
);
ALTER TABLE douban_films
ADD COLUMN country VARCHAR(100)
AFTER release_date;