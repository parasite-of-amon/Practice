-- create database if not exists employees;
-- use employees;

-- create table if not exists employee_address(
-- 	employee_id int,
--     address varchar(50)
-- );

-- alter table employee_address add primary key (employee_id);
-- ------------------------------------------------------------------------------------------------
-- create database if not exists Sale;
-- use Sale;

-- create table if not exists Product(
-- 	product_id int,
--     product_name varchar(50)
-- );

-- create table if not exists Purchase(
-- 	id int,
--     price int 
-- );

-- alter table Pruchase add primary key (id);
------------------------------------------------------------------------------------
-- use employees;
-- insert into employee_address
-- values (1,'69 Somerset Avenue NJ','John');
------------------------------------------------------------------------------------
-- use Sale;
-- insert into product values (300,'Laptop');
-- alter table purchase drop column price;
-- alter table purchase add column price float;
-- insert into purchase values (1,1000.2);

use employees;
insert into employee_address 
values (133, 'K23 Nightwalker Street', 'Evernight'), (140, '420 Southville Drive', 'Mage');

------------------------------------------------------------------------------------

select employee_id, address, first_name from employee_address;
select * from employee_address;

select distinct first_name from employee_address; -- shows unique values only
select first_name from employee_address;

select * from employee_address where first_name='Evernight'; -- shows info related to rates
select * from employee_address where employee_id<=120; -- shows values bounded by integers
------------------------------------------------------------------------------------
select * from employee_address 
where first_name != 'Evernight'; -- negation
select * from employee_address 
where first_name = 'Evernight' or employee_id = 140; -- or logic operator

select * from employee_address
where not employee_id = 1; -- the not logic operator 

select * from employee_address
where employee_id > 100 and employee_id < 135; -- between operator

select * from employee_address
where first_name in ('Evernight','John'); -- in operator 

use Sale;
select * from purchase
where price is not null; -- checking for not null values

select * from purchase
where price is null; -- checking for null value sin table

use employees;
select * from employee_address
order by employee_id Desc; -- ordering by decending terms
