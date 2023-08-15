/* database creation */

drop table if exists news;
drop table if exists member;
drop table if exists classes;

/* create tables */

create table member(
    member_id integer primary key autoincrement not null,
    name text not null,
    email text not null unique,
    password text not null,
    authorisation integer not null
);

create table news(
    news_id integer primary key autoincrement not null,
    title text not null unique,
    subtitle text not null unique,
    content text not null unique,
    newsdate date not null ,
    member_id integer not null,
    foreign key(member_id) references member(member_id)
);

create table classes(
    class_id integer primary key autoincrement not null,
    dayorder integer not null,
    day text not null,
    startdatetime date not null,
    enddatetime date not null,
    title text not null,
    site text not null
);

insert into member( name, email, password, authorisation)
values('Mike', 'm@g.com', 'temp', 0);
insert into member( name, email, password, authorisation)
values('Vanessa', 'vanny@yahoo.com', 'temp', 0);
insert into member( name, email, password, authorisation)
values('Olivia', 'olly66@marsden.com', 'temp', 1);
insert into member( name, email, password, authorisation)
values('Suzie', 'zuzy@qmc.com', 'temp', 1);



insert into news(title, subtitle, content, newsdate, member_id)
values('LA Dance Show',
       'On Sunday the 4th of June',
       'Come along to enjoy a night at the movies, with songs from all your favourite films!' || char(10) ||
       'There''s something for everyone.',
       '2023-05-04 7:00:00',
       (select member_id from member where name='Mike' )
       );

insert into news(title, subtitle, content, newsdate, member_id)
values ('Class Cancelled',
        'This Wednesday 31st May',
        'Advanced One jazz class at 7:15pm until 8:30pm cancelled this week due to illness. ' || char(10) ||
        'This will be made up for at a later date.',
        '2023-05-29 14:00:00',
        (select member_id from member where name = 'Vanessa' )
        );

