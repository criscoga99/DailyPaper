drop database if exists DailyPaper;
create database if not exists DailyPaper;
use DailyPaper;

drop table if exists usuarios;
create table if not exists usuarios(
id smallint unsigned auto_increment not null,
nombre varchar(15) not null,
pass varchar(15) not null,
tipo_usuario enum ('Admin', 'Usuario', 'Editorial'),
constraint pk_usuarios primary key (id)
)engine=InnoDB;

drop table if exists publicaciones;
create table if not exists publicaciones(
id smallint unsigned auto_increment not null,
titular varchar(50),
contenido varchar(250),
creador smallint unsigned not null,
tematica enum ("Naturaleza", "Economía", "Política", "Internacional", "Moda", "Tecnología", "Ciencia", "Otros"),
Fecha_creacion date,
constraint pk_publicaciones primary key (Id),
constraint fk_publicaciones foreign key (creador) references usuarios(id) on update cascade on delete cascade
)engine=InnoDB;

drop table if exists comentarios;
create table if not exists comentarios(
id smallint unsigned auto_increment not null,
contenido varchar(200) not null,
fecha date,
publicaciones smallint unsigned not null,
usuarios smallint unsigned not null,
constraint pk_comentarios primary key (id),
constraint fk1_comentarios foreign key (publicaciones) references publicaciones(id) on update cascade on delete cascade,
constraint fk2_comentarios foreign key (usuarios) references usuarios(id) on update cascade on delete cascade
);