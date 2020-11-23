SET foreign_key_checks = 0;
DROP TABLE IF EXISTS users;
CREATE TABLE users(
id INT primary key auto_increment,
mail_address varchar(100) not null,
first_name varchar(50) not null,
last_name varchar(50) not null,
birthdate date not null,
`role` ENUM('athlete', 'coach'),
password varchar(100) not null
);


drop table if exists trainings;
create table trainings(
id int primary key auto_increment,
date datetime not null,
`athlete_feeback` varchar(255),
`coach_feedback` varchar(255),
athletes_id int,
coaches_id int,
training_types_id int
);

drop table if exists `training_types`;
create table `training_types`(
id int primary key auto_increment,
`name` varchar(50) not null
);


drop table if exists sports;
create table sports(
id int primary key auto_increment,
`name` varchar(50) not null
);


drop table if exists users_to_sports;
create table users_to_sports(
users_id int,
sports_id int,
constraint fk_sports_users_id foreign key (users_id) references users(id),
constraint fk_users_sports_id foreign key (sports_id) references sports(id)
);

drop table if exists exercises;
create table exercises(
id int primary key auto_increment,
exercise varchar(50) not null,
sets int not null,
reps int not null,
rpe float,
trainings_id int
);


drop table if exists reports;
create table reports(
id int primary key auto_increment,
hours_of_sleep float not null,
`kcal_per_day` float not null,
`muscles_fatigue` float not null,
`muscles_soreness` float not null,
`overall_fatigue` float not null,
`comments` varchar(255),
users_id int,
constraint fk_reports_users_id foreign key (users_id) references users(id)
);

drop table if exists genres;
create table genres(
id int primary key auto_increment,
name varchar(255) not null
);


drop table if exists users_to_genres;
create table users_to_genres(
users_id int,
genres_id int,
constraint fk_users_genres_id foreign key (users_id) references users(id),
constraint fk_genres_users_id foreign key (genres_id) references genres(id)
);

alter table trainings
add constraint fk_trainings_coaches_id foreign key (coaches_id) references users(id);

alter table trainings
add constraint fk_trainings_athletes_id foreign key (athletes_id) references users(id);

alter table trainings
add constraint fk_trainings_training_type_id foreign key (training_types_id) references training_types(id);

alter table exercises
add constraint fk_exercises_training_id foreign key (trainings_id) references trainings(id);
SET foreign_key_checks=1