from neo4j import GraphDatabase


class SportsGraph:
    def __init__(self, uri, auth):
        self.driver = GraphDatabase.driver(uri, auth=auth)

    def close(self):
        self.driver.close()

    def _execute_write(self, query, **params):
        with self.driver.session() as session:
            return session.execute_write(lambda tx: tx.run(query, **params).single())

    def _execute_read(self, query, **params):
        with self.driver.session() as session:
            return session.execute_read(lambda tx: tx.run(query, **params))

    def add_sport(self, sport_id, sport_name):
        query = "MERGE (s:Sport {id: $sport_id, name: $sport_name}) RETURN s"
        return self._execute_write(query, sport_id=sport_id, sport_name=sport_name)

    def add_competition(self, sport_id, competition_id, competition_name):
        query = """
        MATCH (s:Sport {id: $sport_id})
        MERGE (c:Competition {id: $competition_id, name: $competition_name})
        MERGE (s)-[:HAS_COMPETITION]->(c)
        RETURN c
        """
        return self._execute_write(query, sport_id=sport_id, competition_id=competition_id, competition_name=competition_name)

    def add_event(self, competition_id, event_id, event_name, start_time, in_play):
        query = """
        MATCH (c:Competition {id: $competition_id})
        MERGE (e:Event {id: $event_id, name: $event_name, start_time: $start_time, in_play: $in_play})
        MERGE (c)-[:HAS_EVENT]->(e)
        RETURN e
        """
        return self._execute_write(query, competition_id=competition_id, event_id=event_id,
                                   event_name=event_name, start_time=start_time, in_play=in_play)

    def add_market(self, event_id, market_id, market_name):
        query = """
        MATCH (e:Event {id: $event_id})
        MERGE (m:Market {id: $market_id, name: $market_name})
        MERGE (e)-[:OFFERS_MARKET]->(m)
        RETURN m
        """
        return self._execute_write(query, event_id=event_id, market_id=market_id, market_name=market_name)

    def add_event_meta(self, competition_id, event_id):
        query = """
        MATCH (c:Competition {id: $competition_id}), (e:Event {id: $event_id})
        CREATE (c)-[:PROMOTES]->(e)
        """
        return self._execute_write(query, competition_id=competition_id, event_id=event_id)

    def get_sports(self):
        query = "MATCH (s:Sport) RETURN s.name AS sport"
        result = self._execute_read(query)
        return [record["sport"] for record in result]

    def get_competitions(self, sport_name):
        query = """
        MATCH (s:Sport {name: $sport_name})<-[:BELONGS_TO]-(c:Competition)
        RETURN c.name AS competition
        """
        result = self._execute_read(query, sport_name=sport_name)
        return [record["competition"] for record in result]

    def get_events(self, competition_name):
        query = """
        MATCH (c:Competition {name: $competition_name})<-[:PART_OF]-(e:Event)
        RETURN e.name AS event, e.startTime AS startTime
        """
        result = self._execute_read(query, competition_name=competition_name)
        return [{"event": record["event"], "startTime": record["startTime"]} for record in result]