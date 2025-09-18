create database if not exists plumbing;
-- imported data from excel sheets manually 
use plumbing;


-- Query 1 
select productname from product;

-- Query 2
select * from orders;
select distinct orderdate from orders;

-- Query 3
select * from product; 

-- Qery 4
select productid, productname, (unitsonorder/unitsinstock) as OrderRatio from product;

-- Query 5
select * from product; 
select productname, unitprice from product where unitprice<50;

-- Query 6
select productname, unitsonorder, unitsinstock 
	from product where unitsonorder >= unitsinstock*0.4; 

-- Query 7
select productname, unitsonorder, unitsinstock 
	from product where unitsonorder >= unitsinstock*0.4 and unitsonorder <= 10; 
                   
-- Query 8 
select * from customer;
select firstname, lastname, city, state from customer where state != 'NJ';
    
-- Query 9 
select firstname, lastname, city, state 
	from customer where (state != 'NJ' or firstname = 'Robert');
    
-- Query 10 
select * from product;
select productname, unitprice, unitsinstock, unitsonorder 
	from product order by unitsinstock desc, unitsonorder desc;
    
    
