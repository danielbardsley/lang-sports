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
            return session.execute_read(lambda tx: list(tx.run(query, **params)))

    def add_sport(self, sport_id, sport_name):
        query = """
        MERGE (s:Sport {id: $sport_id, name: $sport_name}) 
        RETURN s
        """
        return self._execute_write(query, sport_id=sport_id, sport_name=sport_name)

    def add_competition(self, sport_id, competition_id, competition_name):
        query = """
        MATCH (s:Sport {id: $sport_id})
        MERGE (c:Competition {id: $competition_id, name: $competition_name})
        MERGE (s)-[:HAS_COMPETITION]->(c)
        RETURN c
        """
        return self._execute_write(query, sport_id=sport_id, competition_id=competition_id,
                                   competition_name=competition_name)

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

    def add_selection(self, market_id, selection_id, selection_name, selection_price):
        query = """
        MATCH (m:Market {id: $market_id})
        MERGE (s:Selection {id: $selection_id, name: $selection_name, price: $selection_price})
        MERGE (m)-[:HAS_SELECTION]->(s)
        RETURN s
        """
        return self._execute_write(query,
                                   market_id=market_id,
                                   selection_id=selection_id,
                                   selection_name=selection_name,
                                   selection_price=selection_price)

    def add_event_meta(self, competition_id, event_id):
        query = """
        MATCH (c:Competition {id: $competition_id}), (e:Event {id: $event_id})
        MERGE (c)-[:PROMOTES]->(e)
        """
        return self._execute_write(query, competition_id=competition_id, event_id=event_id)

    def add_competition_meta(self, sport_id, competition_id, collection_name):
        query = """
        MERGE (col:Collection {id: $collection_id, name: $collection_name}) 
        WITH col 
        MATCH (s:Sport {id: $sport_id}), (c:Competition {id: $competition_id})
        MERGE (s)-[:HAS_COLLECTION]->(col)
        MERGE (col)-[:HAS_COMPETITION]->(c)
        """
        collection_id = '{sport_id}-{collection_name}'.format(sport_id=sport_id,
                                                              collection_name=collection_name
                                                              .replace(' ', '')
                                                              .lower())
        return self._execute_write(query,
                                   sport_id=sport_id,
                                   collection_id=collection_id,
                                   competition_id=competition_id,
                                   collection_name=collection_name)

    def get_sports(self):
        query = """
        MATCH (s:Sport) RETURN s AS s
        """
        result = self._execute_read(query)
        return [dict(record.get('s')) for record in result]

    def get_live_events(self):
        query = """
        MATCH (s:Sport)-[:HAS_COMPETITION]->(c:Competition)-[:HAS_EVENT]->(e:Event {in_play: true}) 
        RETURN e
        """
        result = self._execute_read(query)
        return [dict(record.get('e')) for record in result]

    def get_competition_events(self, competition_id):
        query = """
        MATCH (c:Competition {id: $competition_id})-[:HAS_EVENT]->(e:Event)
        RETURN e
        """
        result = self._execute_read(query, competition_id=competition_id)
        return [dict(record.get('e')) for record in result]
