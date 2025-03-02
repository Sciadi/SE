---MOVIES
CREATE TABLE public.movies (
	id serial primary key,
	title_id varchar(20) unique not null,
	title text NULL,
	"type" varchar(50) NULL,
	release_year integer NULL,
	genres varchar(128) NULL,
	production_countries varchar(50) NULL,
	seasons real NULL,
	imdb_score real NULL,
	imdb_votes real NULL,
	description text NULL,
	cast text NULL,
    tsv_movie_title tsvector,
    tsv_movie_description tsvector,
	tsv_movie_release_year tsvector,
    tsv_mul_movie_title_description_genere_type_name_character_cast tsvector,
);

create index tsv_movie_title_index on movies using GIN(tsv_movie_title);
create index tsv_movie_description_index on movies using GIN(tsv_movie_description);
create index tsv_movie_release_year_index on movies using GIN(tsv_movie_release_year);
create index tsv_mul_movie_title_description_genere_type_name_character_cast_index on movies using GIN(tsv_mul_movie_title_description_genere_type_name_character_cast);

update movies m
set 
tsv_movie_title=to_tsvector(m.title), 
tsv_movie_description=to_tsvector(m.description),
tsv_movie_release_year=to_tsvector(cast(m.release_year as varchar(10))),
tsv_mpvoe_cast=to_tsvector(cast(m.release_year as varchar(10))),
tsv_mul_movie_title_description_genere_type_name_character_cast=to_tsvector(m.title||' '||m.description||' '||m.genres||' '|| m.type|| ' '|| m."cast");


update movies m 
set "cast" = XX.x
FROM(
select movie_id, string_agg(c.name || ':' || c.character, ', ') as x from credits c
group by movie_id
) as XX 
where m.title_id = XX.movie_id;

update movies m set tsv_mul_movie_title_description_genere_type_name_character_cast=to_tsvector(m.title||' '||m.description||' '||m.genres||' '|| m.type
|| ' '|| m."cast" 
);

---CREDITS
CREATE TABLE public.credits (
	id serial4 NOT NULL,
	movie_id varchar(20) NOT NULL,
	"name" text NULL,
	"character" text NULL,
	"role" text NULL,
	CONSTRAINT credits_pkey PRIMARY KEY (id),
    tsv_credit_name tsvector,
    tsv_credit_character tsvector,
    tsv_credit_role tsvector,
    tsv_mul_credit_name_character tsvector
);
create index tsv_credit_name_index on credits using GIN(tsv_credit_name);
create index tsv_credit_character_index on credits using GIN(tsv_credit_character);
create index tsv_credit_role_index on credits using GIN(tsv_credit_role);
create index tsv_mul_credit_name_character on credits using GIN(tsv_mul_credit_name_character);

update credits c set 
tsv_credit_name=to_tsvector(c.name), 
tsv_credit_character=to_tsvector(c.character),
tsv_credit_role=to_tsvector(c.role), 
tsv_mul_credit_name_character=to_tsvector(c.name||' '||c.character)
;

---MOVIES_CREDITS
CREATE TABLE movies_credits (
    movie_id INT REFERENCES movies(id) ON DELETE CASCADE,
    credit_id INT REFERENCES credits(id) ON DELETE CASCADE,
    PRIMARY KEY (movie_id, credit_id)
);

insert into movies_credits
select m.id, c.id from 
movies m join credits c
on m.title_id= c.movie_id;

--Tolgo i film che non mi danno info su attori
delete from movies m where id not in (select movie_id from movies_credits);



-- ALTRO 





-- Pulire i campi
UPDATE movies
SET title = REPLACE(REPLACE(REPLACE(title, '{', ''), '}', ''), '"', ''),
description = REPLACE(REPLACE(REPLACE(description, '{', ''), '}', ''), '"', '');

UPDATE credits 
SET name = REPLACE(REPLACE(REPLACE(name, '{', ''), '}', ''), '"', ''), 
character = REPLACE(REPLACE(REPLACE(character, '{', ''), '}', ''), '"', '')
;

-- Creo dataset da esportare csv 
select c.name, c."character", m.title, m.type, m.genres, m.release_year, m.seasons, m.imdb_score, m.description 
from movies m 
join credits c on m.title_id = c.movie_id 
;



