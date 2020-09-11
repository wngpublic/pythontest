basic sqlite commands:
- load sqlite db with text data
- .backup
- .archive
- .import
  .mode csv
  .import file.csv
- .dump
  .output sqlformat.txt             # which has create, insert, etc
  .dump
  .exit
- .headers on
- .mode columns
- .read
  .read sqlformat.txt               # which has insert, create, etc
  .exit
  or
  .mode csv
  .import filename.csv
  or
  cat sqlformat.txt | sqlite3 newdatabase.db
- .quit
- .save file      # write in memory db into file
- sqlite3 database.db "select * from somewhere;" > output.txt
- .output output.txt                # start output
  .mode csv
  select * from somewhere;          # statement
  .output                           # stop output
  .mode
- drop
  drop table;                       # delete table
- sqlite3 database.db .dump > out.txt

sqlite3 new_database.db
> .read ../input_data/input_tiny_db.txt         # load first set of data
> .read ../input_data/goods_db.txt              # load second set of data
> .exit                                         # optional
sqlite3 old_database.db
> .output outputsql.txt
> .dump
> .exit

schema for input_tiny_multitable_db.txt
{
instructions:

create table addresses1 ( gid integer primary key autoincrement, id integer, unit integer, addr_num integer, street_id integer, city_id integer, province_id integer, country_id integer, zip text);
create table cities1 ( gid integer primary key autoincrement, id integer, name text, province_id integer, country_id integer);
create table companies1 ( gid integer primary key autoincrement, id integer, govid integer, name text, address_id integer, domainname text, country_id integer);
create table countries1 ( gid integer primary key autoincrement, id integer, name text, abbrev text, prefix integer);
create table departments1 ( gid integer primary key autoincrement, id integer, companyid integer, deptid integer, deptname text, deptcategory text);
create table employees1 ( gid integer primary key autoincrement, govid integer, employee_id integer, company_id integer, email text, dept_id integer, country_id integer, employer_id integer);
create table entities1 ( gid integer primary key autoincrement, govid integer, namefirst text, namelast text, phone text, email text, address_id integer, country_id integer, datestart integer, dateend integer, entity_type integer);
create table provinces1 ( gid integer primary key autoincrement, id integer, name text, country_id integer);
create table streets1 ( gid integer primary key autoincrement, id integer, name text, city_id integer, province_id integer, country_id integer);
create table addresses2 ( gid integer primary key autoincrement, id integer, unit integer, addr_num integer, street_id integer, city_id integer, province_id integer, country_id integer, zip text);
create table cities2 ( gid integer primary key autoincrement, id integer, name text, province_id integer, country_id integer);
create table companies2 ( gid integer primary key autoincrement, id integer, govid integer, name text, address_id integer, domainname text, country_id integer);
create table countries2 ( gid integer primary key autoincrement, id integer, name text, abbrev text, prefix integer);
create table departments2 ( gid integer primary key autoincrement, id integer, companyid integer, deptid integer, deptname text, deptcategory text);
create table employees2 ( gid integer primary key autoincrement, govid integer, employee_id integer, company_id integer, email text, dept_id integer, country_id integer, employer_id integer);
create table entities2 ( gid integer primary key autoincrement, govid integer, namefirst text, namelast text, phone text, email text, address_id integer, country_id integer, datestart integer, dateend integer, entity_type integer);
create table provinces2 ( gid integer primary key autoincrement, id integer, name text, country_id integer);
create table streets2 ( gid integer primary key autoincrement, id integer, name text, city_id integer, province_id integer, country_id integer);

}




drop table <tablename>
.tables
.read filename
.schema <tablename>
.mode column      // subsequent selects print aligned in columns
.header           // turn on headers
.headers on
.headers off
.mode columns
.mode line        // default
.mode csv
.output test.csv
.output stdout
.output <filename>
.databases


get all employees belonging to companyid
select * from employees where company_id = 1;
select employees.employee_id,employees.email,employees.company_id,companies.name from employees join companies on employees.company_id = companies.id where companies.id = 1;

get all employees belonging to executive at companyid
select employees.email,companies.name,departments.deptname
  from employees
  join companies on employees.company_id = companies.id
  join departments on employees.dept_id = departments.deptid and
    companies.id = departments.companyid and
    departments.deptname like 'Executive%';

select employees.email,employees.dept_id,departments.deptname
  from employees
  join departments on departments.deptid = employees.dept_id and
    employees.company_id = departments.companyid and
    departments.companyid = 1;

select count(*) from employees group by company_id;
----------
8         10        8         18        6         12        9




get all executives from all companies






OK
select companies.name, companies.govid, countries.name from companies join countries on countries.id = companies.country_id;
select companies.govid, companies.country_id from companies where companies.govid < 5 limit 10
select govid, country_id from companies where govid in (select govid from companies where govid < 5);
select govid, country_id, companies.name, countries.name from countries, companies;
select govid, country_id, companies.name, countries.name, countries.id from countries, companies where countries.id = 9;
select govid, country_id, companies.name, countries.name, countries.id from countries, companies where countries.id = 9 and country_id = 9;
select govid, country_id, companies.name from companies where country_id = 9;
select * from companies where country_id = 9;
select count(*) from companies where country_id = 9;
select companies.name, companies.domainname, countries.name from companies join countries on companies.country_id = countries.id;
select companies.name, companies.domainname, countries.name from companies join countries on companies.country_id = countries.id order by countries.name;
select * from entities where entities.country_id = 0 and namefirst is null; // namefirst = null does not work
select count(*) from entities where entities.country_id = 0 and address_id is not null;
select * from entities where entities.address_id = 11 and entities.country_id = 0;
delete from tablename;

select streets.name,cities.name,countries.name
  from streets
  join cities on cities.id = streets.id
  join countries on countries.id = streets.country_id
  limit 30;

select count(*) from cities group by country_id;    // correct resulty
select count(*) from cities group by province_id;   // correct result
SELECT * FROM runners WHERE id NOT IN (SELECT winner_id FROM races WHERE winner_id IS NOT null)

group entities by companies for each country.

select entity_type, count(*) from entities;

select entity_type, count(country_id) from entities group by entity_type;

select country_id, count(entity_type) from entities group by country_id;

select country_id, count(entity_type) from entities group by country_id,entity_type;

select country_id, entity_type,count(entity_type) from entities group by country_id,entity_type;

select cities.name as cname,
  cities.province_id,
  provinces.id as pid,
  cities.country_id,
  countries.id as cid,
  provinces.name as pname,
  countries.name as ctryname from cities
  join countries on countries.id = cities.country_id and
    countries.id = provinces.country_id
  join provinces on provinces.id = cities.province_id;

select
    cities.name as cname,
    provinces.name as pname,
    countries.name as ctryname
  from cities
    join countries on countries.id = cities.country_id
    join provinces on provinces.id = cities.province_id and
      countries.id = provinces.country_id;

select
    streets.name as sname,
    cities.name as cname,
    provinces.name as pname,
    countries.name as ctryname
  from cities
    join countries on countries.id = cities.country_id
    join provinces on provinces.id = cities.province_id and
      countries.id = provinces.country_id
    join streets on streets.city_id = cities.id and
      streets.province_id = cities.province_id and
      streets.country_id = cities.country_id;

select
    streets.name as sname,
    cities.name as cname,
    provinces.name as pname,
    countries.name as ctryname
  from cities
    join countries on countries.id = cities.country_id
    join provinces on provinces.id = cities.province_id and countries.id = provinces.country_id
    join streets on streets.city_id = cities.id and streets.province_id = cities.province_id and streets.country_id = cities.country_id
  where cities.name = 'oso2' or cities.name = 'rnr2';

join country name and provinces?
select countries.name, count(provinces.name) from countries join provinces on countries.id = provinces.country_id;
select countries.name, provinces.name from provinces join countries on countries.id = provinces.country_id;

how many provinces for each country in provinces?
yes:
  select provinces.country_id, count(*)
    from provinces group by provinces.country_id;

join country,province,city names:
yes:
  select countries.name,provinces.name,cities.name from cities
    join countries on countries.id = cities.country_id
    join provinces on provinces.id = cities.province_id and provinces.country_id = cities.country_id;

countryname,number of provinces
wrong:
  select countries.name, count(*) from countries
    join provinces on countries.id = provinces.country_id;
  wrong. outputs last country,total count
yes:
  select countries.name, count(*) from provinces
    join countries on provinces.country_id = countries.id
    group by provinces.country_id;

country name, province name, number cities each province:
wrong:
  select countries.name,provinces.name,count(*) from cities
    join countries on countries.id = cities.country_id
    join provinces on provinces.id = cities.province_id and provinces.country_id = cities.country_id
    group by cities.name;
  select countries.name,provinces.name,count(*) from cities
    join countries on countries.id = cities.country_id
    join provinces on provinces.id = cities.province_id and provinces.country_id = cities.country_id
    group by cities.province_id;
yes:
  select countries.name,provinces.name,count(*) from cities
    join countries on countries.id = cities.country_id
    join provinces on provinces.id = cities.province_id and provinces.country_id = cities.country_id
    group by provinces.name;

how many cities in each country? countryname,numcities
wrong:
  select countries.name,count(*) from cities
    join countries on countries.id = cities.country_id
    group by cities.name;
yes:
  select countries.name,count(*) from cities
    join countries on countries.id = cities.country_id
    group by countries.name;

how many provinces and cities in each country?  country,numProvinces,numCitiesInCountry
wrong:
  select countries.name,count(*),from cities

select count(*),province_id from addresses where unit != "" group by province_id;

select count(*),city_id,province_id from addresses where unit != "" group by province_id,city_id;

employees per company:
select count(*),company_id from employees group by company_id;

select count(*),employees.company_id,countries.name
  from employees
  join entities on entities.govid = employees.govid
  join countries on countries.id = entities.country_id
  group by countries.name,employees.company_id
  order by countries.name,employees.company_id;

select employees.email,employees.company_id,countries.name
  from employees
  join entities on entities.govid = employees.govid
  join countries on countries.id = entities.country_id
  where countries.name = 'Country 0'
  order by countries.name,employees.company_id;


addresses of employees by city
workemail entityemail cities.name
join employees,govid with entities.govid and join entities.address_id with addresses.id and join addresses.city_id with cities.id

select employees.email,entities.email,cities.name from employees
  join entities on
    entities.govid = employees.govid and
    entities.country_id = employees.country_id
  join addresses on
    entities.address_id = addresses.id and
    entities.country_id = addresses.country_id
  join cities on
    addresses.city_id = cities.id and
    addresses.country_id = cities.country_id and
    cities.province_id = addresses.province_id and
    entities.country_id = cities.country_id;

select employees.email,entities.email,cities.name from employees join entities on entities.govid = employees.govid and entities.country_id = employees.country_id join addresses on entities.address_id = addresses.id and entities.country_id = addresses.country_id join cities on addresses.city_id = cities.id and addresses.country_id = cities.country_id and cities.province_id = addresses.province_id and entities.country_id = cities.country_id;

count addresses and provinces and name of country

use subqueries to do multiple counts
select
  count(id) as numaddr,
  (
    select
      count(distinct province_id)
    from addresses a
    where
      a.country_id = b.country_id
    group by country_id
  ) as numprov,
  country_id
from addresses b
  group by country_id;



select count(distinct province_id) from addresses group by country_id;

select count(*),province_id,country_id from addresses group by country_id,province_id;

select count(*),country_id from provinces group by country_id;

select a,b,count(a) from tbl group by a,b

find streets that have duplicate names:
maybe:
  select name, count(name) from streets group by name having count(name) > 1;

find addresses that have

countryname,cityname,numCompanies?
wrong:
  companies->address_id->addresses.id->city_id
  select countries.name,cities.name,count(*) from companies
    join countries on countries.id = cities.country_id and countries.id = companies.country_id
    join cities on countries.id = cities.country_id and cities.id = compa

country_id, numCities by using cities table only:
yes:
  select country_id,count(*) from cities group by country_id;

SYNTAX OK BUT WRONG RESULTS:

chooses one row, the last city matching each group of country_id
  select * from cities group by cities.country_id;


select entities.govid,entities.namefirst,entities.namelast,entities.email,streets.name,addresses.addr_num
  from entities
  join streets on streets.country_id = entities.country_id
  join addresses on addresses.id = entities.address_id and
    addresses.country_id = entities.country_id
  where entities.country_id = 0
  limit 10;

select addresses.unit,addresses.addr_num,streets.name,cities.name,provinces.name,countries.name
  from addresses
  join cities on cities.id = streets.id
  join countries on countries.id = streets.country_id
  join provinces on provinces.id = addresses.province_id
  join streets on streets.id = addresses.street_id
  limit 10;

select cities.name,provinces.name,countries.name
  from cities
  inner join provinces on provinces.id = cities.province_id
  inner join countries on countries.id = cities.country_id;

select addresses.unit,addresses.addr_num,streets.name,cities.name,provinces.name,countries.name from addresses
  join cities on cities.id = streets.id
  join countries on countries.id = streets.country_id
  join provinces on provinces.id = addresses.province_id
  join streets on streets.id = addresses.street_id
  where addresses.addr_num = 20;

BAD:
select entities.govid,entities.namefirst,entities.namelast,entities.email,streets.name,addresses.addr_num from entities where entities.country_id = 0 join streets on streets.country_id = entities.country_id join addresses on addresses.id = entities.address_id and addresses.country_id = entities.country_id limit 10;
select companies.name, companies.domainname from companies join (select countries.name from countries) on companies.country_id = countries.id;
select companies.govid, companies.country_id, countries.name from companies where companies.govid < 5 join countries on countries.id = companies.country_id limit 10;
select companies.govid, companies.country_id, countries.name from (select govid from companies where govid < 5) join countries on countries.id = companies.country_id limit 10;
select govid, companies.country_id, name from (select govid from companies where govid < 5) join countries on countries.id = companies.country_id limit 10;
select govid, companies.country_id, name from (select govid from companies where govid < 5) join countries.name, countries.id  on countries.id = companies.country_id limit 10;
select govid, companies.country_id, name from (select govid from companies where govid < 5) join (select countries.name, countries.id from countries) on countries.id = companies.country_id limit 10;
select govid, companies.country_id, name from (select govid from companies where govid < 5) join (select name, id from countries) on countries.id = companies.country_id limit 10;
select companies.govid, companies.country_id, companies.name, countries.name from (select govid from companies where govid < 5) join (select name, id from countries) on countries.id = companies.country_id limit 10;
select govid, country_id, companies.name, countries.name from (select govid from companies where govid < 5) where countries.id = companies.country_id limit 10;
select govid, companies.country_id, companies.name, countries.name from (select govid from companies where govid < 5) where countries.id = companies.country_id limit 10;


select govid, country_id from companies where govid in (select govid from companies where govid < 5) join countries on countries.id = companies.country_id limit 10;


select count(*), quality, category from products group by category,quality;
select * from products where manufacturer_id = 2780 order by category,quality;
select count(*),category from products group by category;
select count(*),category,quality from products group by category,quality order by category;


sql queries for this schema: {

"select countries1,provinces1,cities1":
{
select countries.*,provinces.*,cities.* from countries1 countries,provinces1 provinces,cities1 cities;

this becomes cross product.  countries1 has 4 provinces1 has 7 cities1 has 17
  4 * 7 * 17 = 476 results
},

"join countries1,provinces1,cities1":
{
  select  countries.*, provinces.*, cities.*
    from countries1 countries, provinces1 provinces, cities1 cities
    join countries on (countries.id = provinces.country_id)
    join countries on (countries.id = cities.country_id)
    join cities on (cities.province_id = provinces.id);
},

"join countries1,provinces1":
{

these are wrong but execute: {

wrong
select c.*,p.* from countries1 as c, provinces1 as p join countries1 on c.id = p.country_id;
select c.*,p.* from countries1 as c, provinces1 as p inner join countries1 on c.id = p.country_id;

wrong
select c.*,p.* from countries1 as c, provinces1 as p join provinces1 on c.id = p.country_id;
select c.*,p.* from countries1 as c, provinces1 as p inner join provinces1 on c.id = p.country_id;

wrong
select c.*,p.* from countries1 as c, provinces1 as p join provinces1 on c.id = p.country_id join countries1 on c.id = p.country_id;

wrong
select c.gid,c.id,c.name,c.abbrev,c.prefix,p.gid,p.id,p.name,p.country_id from countries1 as c, provinces1 as p join countries1 on c.id = p.country_id;
select c.gid,c.id,c.name,c.abbrev,c.prefix,p.gid,p.id,p.name,p.country_id from countries1 as c, provinces1 as p join provinces1 on c.id = p.country_id;
select c.gid,c.id,c.name,c.abbrev,c.prefix,p.gid,p.id,p.name,p.country_id from countries1 as c, provinces1 as p inner join provinces1 on c.id = p.country_id;
select c.gid,c.id,c.name,c.abbrev,c.prefix,p.gid,p.id,p.name,p.country_id from countries1 as c, provinces1 as p left join provinces1 on c.id = p.country_id;

select c.gid,c.id,c.name,c.abbrev,c.prefix,p.gid,p.id,p.name,p.country_id from countries1 as c, provinces1 as p left join provinces1 on c.id = p.country_id;

select c.gid,c.id,c.name,c.abbrev,c.prefix,p.gid,p.id,p.name,p.country_id from countries1 as c, provinces1 as p where c.id = p.country_id;

select c.* from countries1 as c join provinces1 as p on c.id = p.country_id;
select c.*,p.* from countries1 as c provinces1 as p inner join p on c.id = p.country_id;

select c.id,c.name,c.abbrev,c.prefix,p.id,p.name,p.country_id from countries1 as c, provinces1 as p inner join provinces1 on p.country_id = c.id;

select c.id,c.name,c.abbrev,c.prefix,p.id,p.name,p.country_id from countries1 as c, provinces1 as p inner join provinces1 as p1 on p1.country_id = c.id;

select c.* from countries1 as c inner join provinces1 as p on p.country_id = c.id;

}

these are correct.
{
select c.gid,c.id,c.name,c.abbrev,c.prefix,p.gid,p.id,p.name,p.country_id from countries1 as c, provinces1 as p where c.id = p.country_id;

select countries1.gid,countries1.id,countries1.name,countries1.abbrev,countries1.prefix,provinces1.gid,provinces1.id,provinces1.name,provinces1.country_id from countries1, provinces1 where countries1.id = provinces1.country_id;

select c.*,p.* from countries1 as c, provinces1 as p where c.id = p.country_id;

}

}

"join countries,provinces,cities": {

this is wrong: {
select c.*,p.*,city.* from countries1 as c, provinces1 as p, cities1 as city where c.id = p.country_id and c.id = city.country_id and p.id = city.province_id;
}

this is right: {

}
}

}


}

{
good sql statements

select * from countries1 inner join provinces1 on countries1.id = provinces1.country_id;

select countries1.id, countries1.name, provinces1.name, provinces1.country_id
  from countries1 inner
  join provinces1 on countries1.id = provinces1.country_id;

// produces same thing
select countries1.id, countries1.name, provinces1.name, provinces1.country_id from countries1 join provinces1 on countries1.id = provinces1.country_id;

.schema cities1
.schema provinces1

join 3 tables

// note it is not 3 joins, but 2 joins with a compound AND
// if use 3 joins on 3 tables, you get ambiguous column name
select
  countries1.id cid, countries1.name as cname,
  provinces1.name as pname, provinces1.id as pid, provinces1.country_id as pcid,
  cities1.name as cityname, cities1.province_id as citypid, cities1.country_id as citycid
from countries1
  join provinces1 on countries1.id = provinces1.country_id
  join cities1 on countries1.id = cities1.country_id and
    provinces1.id = cities1.province_id;

select
  countries1.id cid, countries1.name as cname,
  provinces1.name as pname, provinces1.id as pid, provinces1.country_id as pcid,
  cities1.name as cityname, cities1.province_id as citypid, cities1.country_id as citycid
from countries1
  join provinces1 on cid = pcid
  join cities1 on cid = citycid and pid = citypid;

// cities1 has more cities, so do left join
select
  cities1.gid as cityid, cities1.name as cityname, cities1.province_id as citypid, cities1.country_id as citycid,
  provinces1.name as pname, provinces1.id as pid, provinces1.country_id as pcid,
  countries1.id cid, countries1.name as cname
from cities1
  left join provinces1 on citypid = pid and citycid = pcid
  left join countries1 on cid = citycid;

// seems to produce the same answer as above?
select
  countries1.id cid, countries1.name as cname,
  provinces1.name as pname, provinces1.id as pid, provinces1.country_id as pcid,
  cities1.name as cityname, cities1.province_id as citypid, cities1.country_id as citycid
from countries1, provinces1, cities1
  where cid = pcid and cid = citycid and pid = citypid;


select
  countries1.id cid, countries1.name as cname,
  provinces1.name as pname, provinces1.id as pid, provinces1.country_id as pcid,
  cities1.name as cityname, cities1.province_id as citypid, cities1.country_id as citycid
from countries1
  join provinces1 on cid = pcid
  join cities1 on cid = citycid and pid = citypid
where cid = 0;

select
  countries1.id cid, countries1.name as cname,
  provinces1.id as pid, provinces1.country_id as pcid,
  cities1.province_id as citypid, cities1.country_id as citycid
from countries1
  join provinces1 on cid = pcid
  join cities1 on cid = citycid and pid = citypid
group by cid;

select
  countries1.id cid, countries1.name as cname,
  provinces1.id as pid, provinces1.country_id as pcid,
  cities1.province_id as citypid, cities1.country_id as citycid
from countries1
  join provinces1 on cid = pcid
  join cities1 on cid = citycid and pid = citypid
group by cid, pid;

select
  count(*),
  countries1.id cid, countries1.name as cname,
  provinces1.id as pid, provinces1.country_id as pcid,
  cities1.province_id as citypid, cities1.country_id as citycid
from countries1
  join provinces1 on cid = pcid
  join cities1 on cid = citycid and pid = citypid
group by cid, pid;

select
  countries1.id cid, countries1.name as cname,
  provinces1.name as pname, provinces1.id as pid, provinces1.country_id as pcid,
  cities1.name as cityname, cities1.province_id as citypid, cities1.country_id as citycid
from countries1
  left join provinces1 on cid = pcid
  left join cities1 on cid = citycid and pid = citypid;

select * from addresses1 where unit <> "";
select * from addresses1 where unit != "";  // same as <>
select * from addresses1 where unit <> NULL; // not valid for sqlite3
}

make sure all tables match every relevant field else there will be cross joins!
model_multitable_tiny.db
select * from addresses1
join cities1 on addresses1.city_id = cities1.id
join countries1 on addresses1.country_id = countries1.id and cities1.country_id = countries1.id
join provinces1 on provinces1.country_id = countries1.id and provinces1.id = addresses1.province_id;

select count(*),* from cities group by province_id order by count(*);
select count(*),province_id,country_id from cities group by province_id, country_id order by count(*);

select avg(price),* from products_prices where name = 'fruits' order by price;
select avg(price),count(*),* from products_prices group by name;
select avg(price),count(*),* from products_prices where name = 'fruits' order by avg(price);
select avg(price),count(*),name,product_id from products_prices group by name order by avg(price);
select min(price), * from products_prices group by name order by price;
select max(price), * from products_prices group by name order by price;

update tablename set k1=v1, k2=v2 where k3=id;
select count(*),lastname from entities where (lastname='momo' or lastname='om') group by lastname;
select  sum(case when lastname='momo' then 1 else 0 end) as sum_momo,
        sum(case when lastname='om' then 1 else 0 end) as sum_om,
        lastname from entities where (lastname='momo' or lastname='om') group by lastname;
{
- notes
--  regex
    expr NOT REGEXP pat <=> NOT (expr REGEXP pat)
    REGEXP
    RLIKE
    NO_REGEXP
--- examples
    select * REGEXP '^\w+$'
--- syntax
    a+            match 1 or more
    a*            match 0 or more
    a?            match 0 or 1
    pat1|pat2     alternation,either
    (abc)*        match 0 or more of sequence abc
    (abc){2}      match twice of sequence abc
    (abc){2,3}    match t or 2 times abc
    (abc)+        <=> (abc){1,}
    (abc){1,}     <=> (abc)+
    (abc)?        <=> (abc){0,1}
    [charclass]
--  pattern match but not regex
    LIKE          like 'abc', like 'abc%'
    NOT LIKE      not like 'abc'
    STRCMP
--- in pattern match, % and _ are the only wildcard designations
    %             match any number <=> *
    _             match exactly 1 <=> {1}



--  login
    brew install mysql
    brew reinstall mysql
    /usr/local/mysql/bin/mysql -u ...
    mysql -u root -p <RETURN> // get the prompt for pass
    dont do sudo mysql -u, only mysql -u X -p
    mysqladmin shutdown
    sudo mysqld_safe --skip-grant-tables &  // start mysql with no pw
    sudo /usr/local/mysql/support-files/mysql.server start
    sudo /usr/local/mysql/support-files/mysql.server stop
    /etc/init.d/mysqld start
    /etc/init.d/mysqld stop
    /etc/init.d/mysqld restart
    flush privileges;           // after pw change
--  create table
    create table tablename (
        f1 int autoincrement primary key,
        f2 varchar(100) not null,
        f3 int default 1,
        f4 int,
        f5 enum('e1','e2','e3') default null,
        f6 boolean default false,
        ts timestamp not null default CURRENT_TIMESTAMP,
        index (f3),             // individual index
        index (f4)
    );

    create table tablename (
        f1 int autoincrement primary key,
        f2 varchar(100) not null,
        f3 int default 1,
        f4 int,
        ts timestamp not null default CURRENT_TIMESTAMP,
        index (f3,f4)           // multicolumn index
    );


    describe db.tablename;              // the output format of schema
    show create table db.tablename;     // the sql create statement
    show index from db.tablename;       // show the index format (this + describe)

    varchar(n)
    tinyint(n)
    int(n)
    text
    longtext
    datetime
    timestamp

--- insert/select enum into enum table
    insert into tablename(c1,cenum) values('blah','e1'); // 'e1' is predefined enum value
    insert into tablename(c1,cenum) values('blah',1);    // index 1 == 'e1', 2 == 'e2'
    select * from tablename where cenum = 'e1';
    // dont use enum because of portability. alter is also expensive!

--- select
    // does this work as join instead of join?
    select tbl1.*,tbl2.* from tbl1,tbl2 where tbl1.f1 = tbl2.f1 limit 10;

    select t1.c1,t2.c2 from t1 join t2 on c1=c2;
    select t1.c1,t2.c2 from t1 left join t2 on c1=c2 where c1='x';
    select t1.c1,t2.c2 from t1 left join t2 on t1.c1=t2.c1 and t1.c2 = t2.c2 where c1='x';

    // join 3 tables, test this out to see if it works
    select t1.*,t2.*,t3.* from t1 join t2 on t1.c1=t2.c1 join t3 on t1.c2 = t3.c2 where c1='x';

    select * from t1 where c1 in ('v1','v2');           // multiple match
    select * from t1 where c1 not in ('v1','v2');       // multiple match
    select * from t1 where c1 in (
        select * from t2 group by c2);
    select *, count(*) from t1 group by x;

--- copy
    create table if not exists db.newtablename like db.oldtablename;        // copies indexes and triggers, doesnt overwrite

    create table db.newtablename like db.oldtablename;        // copies indexes and triggers
    insert db.newtablename select * from db.oldtablename;

    create table db.newtablename as select * from db.oldtablename;    // copies column structure and data but not indexes

--- alter/drop table/add column
    // mysql will name the indexes for you even if you dont give one, you can
    alter table <tablename> add column <columnname> <datatype> <datatype qualification> first|after <existingcolumnname>, add index (columnname);
    alter table t1 add column c11 varchar(10) after c10;
    alter table t1 add column c11 varchar(10) not null after c10;
    alter table t1 add column c11 varchar(10) not null default 'abc' after c10;
    alter table t1 add column c11 varchar(10) not null after c10, add index (c11);
    alter table t1 add index [named_indexname] (c11);
    alter table t1 add index (c11); // mysql autonames it unless conflict
    alter table t1 add index indexname (c11,c12,c13);   // multicolumn should be named

    see the column name with: show index from db.tablename;

    creating index after create table:
    create index idxname on tablename(c1);
    create index idxname on tablename(c1,c2,c3);    // multicolumn index
    create index idxname on tablename(c1) using BTREE;

    alter table tablename add index(c1);
    alter table tablename add index(c1,c2);
    alter table tablename add primary key(c1);

    alter table tablename drop column c1,c2;
    drop index idxname on tablename; // use show index from db.tablename to see index names
    drop index `primary` on tablename;


--- delete
    delete from tablename where a = 'b';
    delete from tablename where a in (1,2,3);
    delete from tablename;                              // delete ALL entries from tablename;
    delete from tablename where condition order by c1 limit 100;
    // when deleting, order is not specified, so always delete by order if using limit


    
--  copy table from one database to another, copy data
    create table tabledst like dbsrc.tablesrc;
    create table if not exists tabledst like tablesrc;
    create table tabledst like tablesrc;                      // use this
    create table tabledst select col1,col2 from tablesrc;
    create table tabledst select col1,col2 from tablesrc where condition;
    insert into tabledst select * from tablesrc;              // use this
    insert into dbdst.tabledst select * from dbsrc.tablesrc;
    insert tabledst select * from tablesrc;                   // this looks wrong
    insert into tabledst (col1,col2) select col1,col2 from tablesrc;
    insert into tabledst select * from tablesrc where condition;
    insert into tabledst select * from tablesrc where condition on duplicate key update col1=val;
    insert ignore into tabledst select * from tablesrc where condition;
      // warning and no insert if duplicate key or unique constraints, insert row to partitioned table,
      // but values dont map to a partition
    insert into tabledst 
      select * from tablesrc T1 
      left join tabledst T2 on T1.col_prim = T2.col_prim where T2.col_prim is null;
      // do left join and insert records from T1 to T2 where col_prim don't match
--  add column
    alter table tabledst add column <colname> varchar(255) not null after <existing_col> 
    alter table tabledst add column <colname> varchar(255) not null default 0 after <existing_col> 
    alter table tabledst add column <colname> varchar(255) not null default 0 primary key after <existing_col> 
    alter table tabledst add column <colname> varchar(255) not null default 0
    alter table db.tabledst add primary key(c1,c2,c3);    // make composite primary key
    alter table db.tabledst drop primary key, add primary key(c1,c2,c3); // drop previous primary key, create new composite
    alter table db.tabledst add column col1 int auto increment add primary key(col1); 
    alter table db.tabledst modify column colx int unsigned primary key auto increment;
    alter table db.tabledst drop primary key, add primary key (col1,col2);
    https://dev.mysql.com/doc/refman/5.6/en/alter-table.html
    alter table db.tabledst 
      add column col1 int(5) not null after col3,
      add column col2 int(5) not null after col3;
    
--  dump
    mysqldump -u <u> -p<p> dbname > dump.sql
    mysql -u <u> -p<p> dbname < dump.sql
    mysqldump -u <u> -p<p> dbame tblsrc | mysql -u <u> -p<p> tbldst
--  count rows
    select count(*) from tablesrc;
    select count(col) from tablesrc;
    show table status like 'tablesrc';
    select count(distinct val) from tablesrc;
    select col,count(*) from tablesrc group by col;
    select sum(table_rows) from information_schema.tables where table_schema = '{db}';
    select tablename,tablerows from information_schema.tables where table_schema = '**yourschema**';
--  select distinct c1,c2 from db.tablesrc where c1 is not null and c2 is not null group by c1, order by c1,c2;
    select distinct c1 from db.table <==> select c1 from db.table group by c1;
--  date select
    select * from db.tablesrc where datename > '2020-01-01' limit 100;
--  union
    select c1,c2 from t1 union [all] select c3,c4 from t2; // the columns must have the same type and same order. 
    // all retains duplicates. not having all does not retain duplicate
    


select dist_group, count(*)
from
(
 select case when distance between 0  and 10 then '(0, 10)'
             when distance between 10 and 50 then '(10, 50)'
             ...
             when distance between 5000 and 10000 then '(5000, 10000)' end as dist_group
 from distances
)
group by dist_group

SELECT COUNT( CASE WHEN   0 <= distance AND distance <=   10 THEN distance END ) AS in_range_0_10,
       COUNT( CASE WHEN  10 <  distance AND distance <=   50 THEN distance END ) AS in_range_10_50,
       COUNT( CASE WHEN  50 <  distance AND distance <=  100 THEN distance END ) AS in_range_50_100,
       COUNT( CASE WHEN 100 <  distance AND distance <=  500 THEN distance END ) AS in_range_100_500,
       COUNT( CASE WHEN 500 <  distance AND distance <= 1000 THEN distance END ) AS in_range_500_1000
FROM   Distance

persons:id,last,first,age,city

SELECT Age, COUNT(Age)AS Frequency
  FROM Persons
  GROUP BY Age
  ORDER BY
  COUNT(Age) DESC

select concat(s, '-', e) as range, sum(num) as total, count(*) as num
from ranges
inner join (
   select s.id, count(*) as num
   from subcategory as s
      inner join item as i on i.subcategory = s.id
   where s.category = @category
   group by s.id
) as x on x.num between ranges.s and ranges.e
group by ranges.s, ranges.e

cross join returns combination of possible results. when you cross join,
you're given set containing every possible combination of rows which are
not join restricted. you can use ORDER BY to control the way these data
are returned. or fully join to avoid cross ojin.

inner join drops rows.

select a.a1,b.b1,c.c1 from a
  join c on a.id = c.id
  join b on a.id = b.id
  where a.id = b.id
union
select d.d1,e.e1 from d
  join d on d.id = e.id
  join a.id = d.id

you can also replace join with where clauses

select a.a1,b.b1,c.c1 from a
  where a.id = b.id and
  b.id = c.id and
  a.id = c.id
union
select ...


copy table:
{
  CREATE TABLE IF NOT EXISTS new_table LIKE existing_table;
  INSERT new_table SELECT * FROM existing_table;
}

select all distinct rows selected by either query:
SELECT * FROM
(SELECT NAME FROM EMP WHERE JOB = 'blah2' UNION SELECT NAME FROM EMP WHERE JOB = 'blah1'); 


select all rows, including duplicates, selected by either query:
SELECT * FROM (SELECT SAL FROM EMP WHERE JOB = 'v1' UNION SELECT SAL FROM EMP WHERE JOB = 'v2'); 

select all distinct rows selected by both queries:
SELECT * FROM orders_list1 INTERSECT SELECT * FROM orders_list2 

select all distinct rows from first query minus the rows from the second:
SELECT * FROM (SELECT SAL FROM EMP WHERE JOB = 'v1' MINUS SELECT SAL FROM EMP WHERE JOB = 'v2'); 


}

{
- hive notes

select count(*),c1 from db1.t1 where condition group by x;
select * from db1.t1 lateral view explode(c1_array) v as aliasname where condition;
select * from db1.t1 lateral view json_path_tuple(c1,"$.json_key") v as aliasname where x like '%Y%';
select * from db1.t1 lateral view explode(c1_array) v as alias1 lateral view explode (alias1.json_struct) v2 as alias2 lateral view json_path_tuple(alias2,"$.key") v3 as alias3 where condition;
select * from db1.t1 where c1 rlike 'X';
select * from t1 join t2 on t1.c1 = t2.c1 where condition;
select * from t1 join t2 on t1.c1 = t2.c1 join t3 on t1.c1 = t3.c1 and t2.c1 = t3.c1 where condition;

presto notes
select * from db.table cross join unnest(djsonarray) as a (datastruct) where datastruct.x='y' and a='b' limit 10;



}

