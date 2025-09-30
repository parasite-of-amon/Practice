use plumbing;
select * from customer;
select * from orderdetail;
select * from orders;
select * from product;

# Query 1
select
  c.FirstName as first_name,
  c.LastName  as last_name,
  MIN(p.UnitsInStock) AS Min_UnitInStock,
  MAX(p.UnitsOnOrder) AS Max_UnitOnOrder
from customer as c
join orders as o on o.CustomerID = c.CustomerID
join orderdetail as d on d.OrderID   = o.OrderID
join product as p on p.ProductID  = d.ProductID
group by c.CustomerID, c.FirstName, c.LastName;

# Query 2
select
  c.FirstName as First_Name,
  c.LastName  as Last_Name,
  COUNT(DISTINCT o.OrderID) as Total_Orders
from customer as c
join orders as o on o.CustomerID = c.CustomerID
group by c.CustomerID, c.FirstName, c.LastName
having COUNT(distinct o.OrderID) > 2;

# Query 3
select
  c.FirstName as First_Name,
  c.LastName  as Last_Name,
  AVG(od.UnitPrice) as Average_UnitPrice
from customer as c
join orders as o on o.CustomerID = c.CustomerID
join orderdetail od on od.OrderID = o.OrderID
group by c.CustomerID, c.FirstName, c.LastName;


