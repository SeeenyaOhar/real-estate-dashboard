CREATE KEYSPACE test 
   WITH REPLICATION = { 
      'class' : 'SimpleStrategy', 'replication_factor' : 1 };

use test;
create table test.rent_by_neighbourhood
(
    neighbourhood  text,
    rent_id        text,
    area           int,
    baths_number   int,
    beds_number    int,
    days_on_market int,
    listing_link   text,
    price          int,
    rooms_number   int,
    timestamp      timestamp,
    title          text,
    primary key (neighbourhood, rent_id)
);

create table test.amenities_by_rent
(
    amenity_title  text,
    rent_id        text,
    area           int,
    baths_number   int,
    beds_number    int,
    days_on_market int,
    listing_link   text,
    price          int,
    rooms_number   int,
    timestamp      timestamp,
    title          text,
    primary key (amenity_title, rent_id)
);


create table test.rent
(
    rent_id        text,
    area           int,
    baths_number   int,
    beds_number    int,
    days_on_market int,
    listing_link   text,
    price          int,
    rooms_number   int,
    timestamp      timestamp,
    title          text,
    primary key (rent_id, price, title)
);