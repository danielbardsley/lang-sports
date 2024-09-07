// Define node labels
CREATE CONSTRAINT FOR (s:Sport) REQUIRE s.id IS UNIQUE;
CREATE CONSTRAINT FOR (c:Competition) REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT FOR (e:Event) REQUIRE e.id IS UNIQUE;
CREATE CONSTRAINT FOR (m:Market) REQUIRE m.id IS UNIQUE;
CREATE CONSTRAINT FOR (sel:Selection) REQUIRE sel.id IS UNIQUE;


CREATE (s:Sport {name: 'Football'})

MATCH (s:Sport {name: 'Football'})
CREATE (s)<-[:BELONGS_TO]-(c:Competition {id: 'EPL2024', name: 'English Premier League 2024'})

MATCH (c:Competition {id: 'EPL2024'})
CREATE (c)<-[:PART_OF]-(e:Event {id: 'EVT1', name: 'Manchester City vs Arsenal', startTime: datetime('2023-04-26T20:00:00')})
CREATE (c)<-[:PART_OF]-(e2:Event {id: 'EVT2', name: 'Bournemouth vs Newcastle', startTime: datetime('2023-04-26T21:30:00')})

