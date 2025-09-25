create database if not exists sports;
use sports;

# Query 1
select * from PLAYER;

select p.FirstName, p.LastName, p.PhoneNumber, t.Nickname as TeamNickname
from PLAYER p
join TEAM t on p.TeamID = t.TeamID
where p.Rating = 'A'
order by t.Nickname ASC, p.LastName ASC;

# Query 2
select * from PLAYER;

select t.Nickname, COUNT(*) as NumPlayers
from PLAYER p
join TEAM t on p.TeamID = t.TeamID
group by t.TeamID, t.Nickname
having COUNT(*) >= 3
order by t.Nickname ASC;

# Query 3
select * from TEAM;
select * from PLAYER;

select t.TeamID, t.Nickname, COUNT(*) as NumABPlayers
from PLAYER as p
join TEAM t on p.TeamID = t.TeamID
where p.Rating in ('A','B')
group by t.TeamID, t.Nickname
having COUNT(*) > 0
order by NumABPlayers DESC, t.Nickname ASC;


# Query 4
select * from coach;

select c.FirstName, c.LastName, t.Nickname as TeamNickname
from COACH as c
left join TEAM t on c.TeamID = t.TeamID
order by c.LastName ASC, c.FirstName ASC;

# Query 5
select * from TEAM;
select * from COACH;

select t.TeamID, t.Nickname, COUNT(c.CoachID) as NumCoaches
from TEAM as t
left join COACH c on c.TeamID = t.TeamID
group by t.TeamID, t.Nickname
order by t.TeamID ASC;


