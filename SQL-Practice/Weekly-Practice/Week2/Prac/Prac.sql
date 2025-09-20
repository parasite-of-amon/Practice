create database if not exists play;
use play;

select * from coach;
select * from coach where (teamid = 1 or teamid = 3 or teamid = 4);

-- best (alternate) way 
select * from coach where teamid in (1,3,4); 

-- alias 'as'
select coachid, firstname as FN, lastname as LN, teamid as TI
	from coach where teamid in (1,3,4); 
    
select * from coach; -- original table s not changed due to alias 

-- instead of temporary, we can define alias for tables 
-- (important when we want to join two tables)
select c.coachid, c.firstname, c.lastname, c.address
	from coach c order by c.address;
    
-- concatination 
select concat_ws(', ',lastname, firstname) as 'Full Name'
	from coach order by 'Full Name';
    
-- SQL Server Joints    
-- ----------------------------------------------------------------------------------------------------
select p.PlayerID, p.FirstName, p.LastName, t.Nickname, t.Colors
	from Player as p
    inner join Team as t on p.TeamID = t.TeamID;
-- don't use other way in pdf

-- using clause (not recommended)
select PlayerID, FirstName, LastName, Nickname, Colors
	from Player 
    inner join Team using (TeamID);
    
-- bonus (joining 3 tables)
select p.PlayerID, p.FirstName, p.LastName, t.Nickname, t.Colors, g.DatePlayed, g.HomeTeamID
	from Player as p
    inner join Team as t on p.TeamID = t.TeamID
    inner join Game as g on t.TeamID = g.HomeTeamID;
    
# inner join 3 Tables + Order
select p.PlayerID, p.FirstName, p.LastName, t.Nickname, t.Colors, g.DatePlayed, g.VisitTeamID
	from Player as p
    inner join Team as t on p.TeamID = t.TeamID
    inner join Game as g on t.TeamID = g.VisitTeamID
    order by g.VisitTeamID;
    
# Notice that some of the players are removed with inner join 
# This is becuase they are not assigned a team-id
select PlayerID, FirstName, LastName, Nickname, Colors
	from Player 
    left join Team using (TeamID);
    
ALTER TABLE Player 
MODIFY TeamID INT NULL;

# right and left join are the same but have reversed table definitions
select PlayerID, FirstName, LastName, Nickname, Colors
	from Player 
    right join Team using (TeamID);
    
#calculated expression
select * from player; select * from game;
select HomeScore + VisitScore as TotalScore from Game;
    
select VisitScore / HomeScore as VisitRatio from Game;
    
select max(VisitScore) as MaxVisitScore from Game;
    
   
