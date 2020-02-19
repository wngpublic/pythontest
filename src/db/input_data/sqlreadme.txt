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

addresses         ( id,     unit,         addr_num,     street_id, city_id, province_id, country_id, zip );
streets           ( id,     name,         city_id,      province_id,  country_id );
cities            ( id,     name,         province_id,  country_id );
provinces         ( id,     name,         country_id );
countries         ( id,     name,         abbrev,       prefix );
companies         ( id,     govid,        name,         address_id,   domainname, country_id );
departments       ( id,     companyid,    deptid,       deptname,     deptcategory );
employees         ( govid,  employee_id,  company_id,   email,        dept_id,    country_id, employer_id );
entities          ( govid,  namefirst,    namelast,     phone,        email,      gender, address_id,     country_id, datestart, dateend, entity_type );
products          ( sku,company_product_id,version,quality,category,description,manufacturer_id,country_id,price_cost,price_sale,seller_id,seller_country_id)
receipts_seller   ( date,id,sales_record_id,from_country_id,from_company_id,qty,price_per_item,price_total,to_entity_id,to_country_id,product_id,category_id,version)
receipts_customer ( date,id,sales_record_id,from_country_id,from_company_id,qty,price_per_item,price_total,to_entity_id,to_country_id,product_id,category_id)

db details snapshot:
9 countries
0 2  companies   14 cities  5 provinces
1 8  companies   20 cities  5 provinces
2 3  companies   15 cities  4 provinces
3 2  companies   7  cities  2 provinces
4 2  companies   8  cities  2 provinces
5 9  companies   14 cities  4 provinces
6 6  companies   6  cities  2 provinces
7 2  companies   5  cities  2 provinces
8 12 companies   10 cities  3 provinces
9 13 companies   12 cities  3 provinces

create table addresses ( gid integer primary key autoincrement, id integer, unit integer, addr_num integer, street_id integer, city_id integer, province_id integer, country_id integer, zip text);
create table cities ( gid integer primary key autoincrement, id integer, name text, province_id integer, country_id integer);
create table companies ( gid integer primary key autoincrement, id integer, govid integer, name text, address_id integer, domainname text, country_id integer);
create table countries ( gid integer primary key autoincrement, id integer, name text, abbrev text, prefix integer);
create table departments ( gid integer primary key autoincrement, id integer, companyid integer, deptid integer, deptname text, deptcategory text);
create table employees ( gid integer primary key autoincrement, govid integer, employee_id integer, company_id integer, email text, dept_id integer, country_id integer, employer_id integer);
create table entities ( gid integer primary key autoincrement, govid integer, namefirst text, namelast text, phone text, email text, gender text, address_id integer, country_id integer, datestart integer, dateend integer, entity_type integer);
create table provinces ( gid integer primary key autoincrement, id integer, name text, country_id integer);
create table streets            ( gid integer primary key autoincrement, id integer, name text, city_id integer, province_id integer, country_id integer);
create table products           ( gid integer primary key autoincrement, sku integer,company_product_id integer,version integer,quality integer,category integer,description text,manufacturer_id integer,country_id integer,price_cost integer,price_sale integer,seller_id integer,seller_country_id integer);
create table receipts_seller    ( gid integer primary key autoincrement, date integer, id integer,sales_record_id integer,from_country_id integer,from_company_id integer,qty integer,price_per_item integer,price_total integer,to_entity_id integer,to_country_id integer,product_id integer,category_id integer,version integer);
create table receipts_customer  ( gid integer primary key autoincrement, date integer,id integer,sales_record_id integer,from_country_id integer,from_company_id integer,qty integer,price_per_item integer,price_total integer,to_entity_id integer,to_country_id integer,product_id integer,category_id integer);

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

from online:
select distinct ProductName, UnitPrice from products where UnitPrice>(select avg(UnitPrice) from products) order by UnitPrice desc;

select OrderID, CustomerID from orders where ShippedDate = (select max(ShippedDate) from orders);

select ProductID, ProductName, concat((UnitsInStock / (select sum(UnitsInStock) from products))*100, '%') as Percent_of_total_units_in_stock from products order by ProductID;

select a.ShipperID, a.CompanyName, b.Freight from shippers as a inner join orders as b on a.ShipperID=b.ShipVia where b.Freight = (select max(Freight) from orders);

select distinct a.ProductID, a.UnitPrice as Max_unit_price_sold from order_details as a where a.UnitPrice = ( select max(UnitPrice) from order_details as b where a.ProductID = b.ProductID) order by a.ProductID;

select distinct a.ProductID, a.UnitPrice as Max_unit_price_sold from order_details as a inner join ( select ProductID, max(UnitPrice) as Max_unit_price_sold from order_details group by ProductID) as b on a.ProductID=b.ProductID and a.UnitPrice=b.Max_unit_price_sold order by a.ProductID;

select distinct a.ProductID, p.ProductName, a.UnitPrice as Max_unit_price_sold from order_details as a inner join products as p on a.ProductID = p.ProductID where a.UnitPrice = ( select max(UnitPrice) from order_details as b where a.ProductID = b.ProductID) order by a.ProductID;

select a.OrderID, a.CustomerID from orders as a where ( select Quantity from order_details as b where a.OrderID = b.OrderID and b.ProductID = 6) > 20;

select CustomerID, CompanyName from customers as a where exists ( select * from orders as b where a.CustomerID = b.CustomerID and ShipCountry = 'UK');

select CustomerID, CompanyName from customers as a where not exists
(
    select * from orders as b where a.CustomerID = b.CustomerID and ShipCountry <> 'UK'
);

select distinct a.CustomerID, a.CompanyName from customers as a left join orders as b on a.CustomerID = b.CustomerID where b.ShipCountry = 'UK' or b.ShipCountry is null;

select x.ProductID, y.ProductName, x.max_unit_price from
( select ProductID, max(UnitPrice) as max_unit_price from order_details group by ProductID) as x inner join products as y on x.ProductID = y.ProductID

select ProductID, ProductName, concat((UnitsInStock / (select sum(UnitsInStock) from products))*100, '%') as Percent_of_total_units_in_stock from products order by ProductID;

select ProductID, ProductName, concat((UnitsInStock / 3119)*100, '%') as Percent_of_total_units_in_stock from products order by ProductID;

select CustomerID, CompanyName from customers where CustomerID in
( select CustomerID from orders where orderDate > '1998-05-01');

select a.CustomerID, a.CompanyName from customers as a inner join orders as b on a.CustomerID = b.CustomerID where b.orderDate > '1998-05-01'

select EmployeeID, FirstName, LastName, City, Country from employees where row(City, Country) in (select City, Country from customers);

select distinct a.ProductID, a.UnitPrice as Max_unit_price_sold from order_details as a inner join
( select ProductID, max(UnitPrice) as Max_unit_price_sold from order_details group by ProductID) as b
on a.ProductID=b.ProductID and a.UnitPrice=b.Max_unit_price_sold order by a.ProductID;

select y.CategoryID, y.CategoryName, round(x.actual_unit_price, 2) as "Actual Avg Unit Price", round(y.planned_unit_price, 2) as "Would-Like Avg Unit Price" from
(
    select avg(a.UnitPrice) as actual_unit_price, c.CategoryID from order_details as a inner join products as b on b.ProductID = a.ProductID inner join categories as c on b.CategoryID = c.CategoryID group by c.CategoryID
) as x
inner join
(
    select a.CategoryID, b.CategoryName, avg(a.UnitPrice) as planned_unit_price from products as a inner join categories as b on b.CategoryID = a.CategoryID group by a.CategoryID
) as y on x.CategoryID = y.CategoryID

select * from sql.oilrsrvs o where exists (select Continent from sql.countries c where o.Country = c.Name and Continent = 'Africa');

select * from sql.oilrsrvs o where 'Africa' = (select Continent from sql.countries c where c.Name = o.Country);

select name 'Country', Population format=comma15.  from sql.countries where Name in (select Country from sql.oilprod);

select Name 'State' , population format=comma10.  from sql.unitedstates where population gt (select population from sql.countries where name = "Belgium");

select Name 'State', population format=comma10.  from sql.unitedstates where population gt 10162614;

select s_name, score, status, address_city, email_id, accomplishments from student s inner join marks m on s.s_id = m.s_id inner join details d on d.school_id = m.school_id;

select s_name, score, status, address_city, email_id, accomplishments from student s, marks m, details d where s.s_id = m.s_id and m.school_id = d.school_id;

SELECT wp_woocommerce_order_items.order_id As No_Commande
FROM  wp_woocommerce_order_items
LEFT JOIN
    (
        SELECT meta_value As Prenom, post_id  -- <----- this
        FROM wp_postmeta
        WHERE meta_key = '_shipping_first_name'
    ) AS a
ON wp_woocommerce_order_items.order_id = a.post_id
WHERE  wp_woocommerce_order_items.order_id =2198

SELECT <fieldlist>  FROM Faculty AS f
INNER JOIN Division AS d ON d.FacultyID = f.FacultyID
INNER JOIN Country AS c ON c.FacultyID = f.FacultyID
INNER JOIN Nationality AS n ON n.FacultyID = f.FacultyID

SELECT A.SalesOrderID, B.Foo
FROM A
JOIN B bo ON bo.id = (
     SELECT TOP 1 id
     FROM B bi
     WHERE bi.SalesOrderID = a.SalesOrderID
     ORDER BY bi.whatever
     )
WHERE A.Date BETWEEN '2000-1-4' AND '2010-1-4'

select count(*) from departments;
117

select count(*) from departments where deptcategory = 'R&D';
59

select count(*) from departments where deptcategory != 'R&D';
58

select count(*) from departments where deptcategory like 'Executive';
7

select count(*) from departments group by companyid;
22 10 9 19 13 23 21

select count(*) from companies;
7

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
entity_type  count(*)
-----------  ----------
2            107

select entity_type, count(country_id) from entities group by entity_type;
entity_type  count(country_id)
-----------  -----------------
1            7
2            100

select country_id, count(entity_type) from entities group by country_id;
country_id  count(entity_type)
----------  ------------------
0           31
1           30
2           46

select country_id, count(entity_type) from entities group by country_id,entity_type;
country_id  count(entity_type)
----------  ------------------
0           2
0           29
1           2
1           28
2           3
2           43

select country_id, entity_type,count(entity_type) from entities group by country_id,entity_type;
country_id  entity_type  count(entity_type)
----------  -----------  ------------------
0           1            2
0           2            29
1           1            2
1           2            28
2           1            3
2           2            43




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
count(*)    province_id
----------  -----------
2           0
10          1
5           2

select count(*),city_id,province_id from addresses where unit != "" group by province_id,city_id;
count(*)    city_id     province_id
----------  ----------  -----------
2           1           0
6           2           1
2           3           1
2           5           1
2           5           2
3           7           2

employees per company:
select count(*),company_id from employees group by company_id;
count(*)    company_id
----------  ----------
8           0
10          1
8           2
18          3
6           4
12          5
9           6


select count(*),employees.company_id,countries.name
  from employees
  join entities on entities.govid = employees.govid
  join countries on countries.id = entities.country_id
  group by countries.name,employees.company_id
  order by countries.name,employees.company_id;

count(*)    company_id  name
----------  ----------  ----------
1           4           Country 0
12          5           Country 0
...

select employees.email,employees.company_id,countries.name
  from employees
  join entities on entities.govid = employees.govid
  join countries on countries.id = entities.country_id
  where countries.name = 'Country 0'
  order by countries.name,employees.company_id;

email                  company_id  name
---------------------  ----------  ----------
jyw.mhul.5@company2.2  4           Country 0
hpo.tblc.11@company0.  5           Country 0
oof.chqn.0@company0.0  5           Country 0
...

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
numaddresses  numprovinces  countryname
8             3             c0              8 addresses in 3 provinces in c0
6             2             c1              6 addresses in 2 provinces in c1

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

numaddr     numprov     country_id
----------  ----------  ----------
42          4           0
30          3           1
49          4           2
33          3           3


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

schema for input_tiny_multitable_db.txt
{

schema summary
addresses1/2    ( gid integer,
                  id integer,
                  unit integer,
                  addr_num integer,
                  street_id integer,
                  city_id integer,
                  province_id integer,
                  country_id integer,
                  zip text);
cities1/2       ( gid integer,
                  id integer,
                  name text,
                  province_id integer,
                  country_id integer);
companies1/2    ( gid integer,
                  id integer,
                  govid integer,
                  name text,
                  address_id integer,
                  domainname text,
                  country_id integer);
countries1/2    ( gid integer,
                  id integer,
                  name text,
                  abbrev text,
                  prefix integer);
departments1/2  ( gid integer,
                  id integer,
                  companyid integer,
                  deptid integer,
                  deptname text,
                  deptcategory text);
employees1/2    ( gid integer,
                  govid integer,
                  employee_id integer,
                  company_id integer,
                  email text,
                  dept_id integer,
                  country_id integer,
                  employer_id integer);
entities1/2     ( gid integer,
                  govid integer,
                  namefirst text,
                  namelast text,
                  phone text,
                  email text,
                  address_id integer,
                  country_id integer,
                  datestart integer,
                  dateend integer,
                  entity_type integer);
provinces1/2    ( gid integer,
                  id integer,
                  name text,
                  country_id integer);
streets1/2      ( gid integer,
                  id integer,
                  name text,
                  city_id integer,
                  province_id integer,
                  country_id integer);

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

provinces1 has 7 entries
cities1 has 17 entries
countries1 has 4 entries

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
update cities set name='mad3', province_id=1 where gid=2;
{
- characteristics of input_tiny_db.txt

countries: 4
  id, name, abbrev, prefix
provinces: 14
  id, name, country_id
  select count(*), country_id from provinces group by country_id;
cities: 34 cities
  id, name, province_id, country_id
  select count(*), province_id, country_id from cities group by province_id, country_id;
streets: 52
  id, name, city_id, province_id, country_id
addresses: 154
  id, unit, addr_num, street_id, city_id, province_id, country_id, zip
entities: 241
  govid, namefirst, namelast, phone, email, address_id, country_id,
  datestart, dateend, entity_type
companies: 10
  id, govid, name, address_id, domainname, country_id
departments: 121
  id, companyid, deptid, deptname, deptcategory
employees: 136
  govid, employee_id, company_id, email, dept_id, country_id, employer_id



}
