create table player (player_id int not null auto_increment,team_id int default null,league_id int not null,player_name varchar(45) not null,position varchar(45) not null,age int not null,primary key (player_id),foreign key (team_id) references team (team_id),foreign key (league_id) references league (league_id));
create table team (team_id int not null auto_increment,team_name int default null,league_id int not null,primary key (team_id),foreign key (league_id) references league (league_id));
create table temp create table temp (team_id int not null auto_increment,team_name int default null,league_id int not null,primary key (team_id));
create table temp (team_id int not null auto_increment,team_name int default null,league_id int not null,primary key (team_id));
create table temp (team_id int not null auto_increment,team_name int default null,league_id int not null,primary key (team_id));
create table temp3 (team_id int not null auto_increment,team_name int default null,league_id int not null,primary key (team_id));
